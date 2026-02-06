"""
Report routes - Building finance and other reports
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional

router = APIRouter(tags=["Reports"])


@router.get("/reports/building-finance")
async def get_building_finance(
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None, ge=2020)
):
    """
    Tổng thu chi tòa nhà.
    
    Returns:
    - total_revenue: Tổng thu từ hóa đơn
    - total_expense: Tổng chi (lương nhân viên)
    - net_profit: Lợi nhuận
    """
    try:
        from api.database import get_pool
        
        pool = get_pool()
        
        # Build date filter
        where_clause = ""
        params = []
        
        if month and year:
            where_clause = "WHERE EXTRACT(MONTH FROM i.from_date) = $1 AND EXTRACT(YEAR FROM i.from_date) = $2"
            params = [month, year]
        
        # Total revenue from invoices
        revenue_query = f"""
            SELECT COALESCE(SUM(total_amount), 0) as total_revenue
            FROM invoices i
            {where_clause}
        """
        
        # Total expense (salaries)
        expense_query = """
            SELECT COALESCE(SUM(base_salary), 0) as total_expense
            FROM building_employees
            WHERE status = 'working'
        """
        
        async with pool.acquire() as conn:
            revenue_result = await conn.fetchrow(revenue_query, *params)
            expense_result = await conn.fetchrow(expense_query)
            
            total_revenue = float(revenue_result['total_revenue'])
            total_expense = float(expense_result['total_expense'])
            
            return {
                "month": month,
                "year": year,
                "total_revenue": total_revenue,
                "revenue_breakdown": {
                    "rent": total_revenue * 0.65,  # Estimate 65% from rent
                    "services": total_revenue * 0.35  # Estimate 35% from services
                },
                "total_expense": total_expense,
                "net_profit": total_revenue - total_expense
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/reports/building-finance/details")
async def get_building_finance_details(
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None, ge=2020)
):
    """
    Chi tiết thu chi tòa nhà.
    
    Returns:
    - revenue_details: Chi tiết từng hóa đơn
    - expense_details: Chi tiết lương nhân viên
    """
    try:
        from api.database import get_pool
        
        pool = get_pool()
        
        # Build date filter
        where_clause = ""
        params = []
        
        if month and year:
            where_clause = "WHERE EXTRACT(MONTH FROM i.from_date) = $1 AND EXTRACT(YEAR FROM i.from_date) = $2"
            params = [month, year]
        
        # Revenue details - Join invoices with rent_contracts to get company
        revenue_query = f"""
            SELECT 
                i.id as invoice_id,
                i.total_amount,
                i.from_date,
                i.to_date,
                i.status,
                c.name as company_name,
                c.tax_code
            FROM invoices i
            JOIN rent_contracts rc ON i.id = rc.invoice_id
            JOIN companies c ON rc.company_id = c.id
            {where_clause}
            ORDER BY i.from_date DESC
        """
        
        # Expense details (salaries)
        expense_query = """
            SELECT 
                be.employee_id as id,
                CONCAT(be.first_name, ' ', be.last_name) as full_name,
                be.role as position,
                be.base_salary,
                0.05 as bonus_rate,
                COALESCE(
                    (SELECT SUM(cmu.price * cmu.quantity)
                     FROM company_monthly_usages cmu
                     WHERE cmu.service_id IN (
                         SELECT ss.service_id 
                         FROM service_subscribers ss 
                         WHERE ss.employee_id = be.employee_id
                     )), 0
                ) as service_revenue,
                (be.base_salary + COALESCE(
                    (SELECT SUM(cmu.price * cmu.quantity)
                     FROM company_monthly_usages cmu
                     WHERE cmu.service_id IN (
                         SELECT ss.service_id 
                         FROM service_subscribers ss 
                         WHERE ss.employee_id = be.employee_id
                     )), 0
                ) * 0.05) as total_salary
            FROM building_employees be
            WHERE be.status = 'working'
            ORDER BY total_salary DESC
        """
        
        async with pool.acquire() as conn:
            revenue_rows = await conn.fetch(revenue_query, *params)
            expense_rows = await conn.fetch(expense_query)
            
            total_revenue = sum(float(row['total_amount']) for row in revenue_rows)
            total_expense = sum(float(row['total_salary']) for row in expense_rows)
            
            return {
                "month": month,
                "year": year,
                "total_revenue": total_revenue,
                "total_expense": total_expense,
                "net_profit": total_revenue - total_expense,
                "revenue_details": [
                    {
                        "invoice_id": row['invoice_id'],
                        "company_name": row['company_name'],
                        "tax_code": row['tax_code'],
                        "total_amount": float(row['total_amount']),
                        "from_date": row['from_date'].isoformat(),
                        "to_date": row['to_date'].isoformat(),
                        "status": row['status']
                    }
                    for row in revenue_rows
                ],
                "expense_details": [
                    {
                        "employee_id": row['id'],
                        "full_name": row['full_name'],
                        "position": row['position'],
                        "base_salary": float(row['base_salary']),
                        "bonus_rate": float(row['bonus_rate']),
                        "service_revenue": float(row['service_revenue']),
                        "total_salary": float(row['total_salary'])
                    }
                    for row in expense_rows
                ]
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
