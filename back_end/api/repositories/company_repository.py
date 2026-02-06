"""
Repository for Company entity.
All database operations use raw SQL with asyncpg.
"""
from typing import List, Optional, Dict, Any
from api.database import get_pool


class CompanyRepository:
    """Repository for Company CRUD operations."""
    
    async def create(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new company."""
        query = """
            INSERT INTO companies (name, tax_code, email, address)
            VALUES ($1, $2, $3, $4)
            RETURNING id, name, tax_code, email, address
        """
        async with get_pool().acquire() as conn:
            row = await conn.fetchrow(
                query,
                company_data["name"],
                company_data["tax_code"],
                company_data.get("email"),
                company_data.get("address")
            )
            return dict(row)
    
    async def get_by_id(self, company_id: int) -> Optional[Dict[str, Any]]:
        """Get company by ID."""
        query = "SELECT * FROM companies WHERE id = $1"
        async with get_pool().acquire() as conn:
            row = await conn.fetchrow(query, company_id)
            return dict(row) if row else None
    
    async def get_by_tax_code(self, tax_code: str) -> Optional[Dict[str, Any]]:
        """Get company by tax code."""
        query = "SELECT * FROM companies WHERE tax_code = $1"
        async with get_pool().acquire() as conn:
            row = await conn.fetchrow(query, tax_code)
            return dict(row) if row else None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all companies with pagination."""
        query = "SELECT * FROM companies ORDER BY id LIMIT $1 OFFSET $2"
        async with get_pool().acquire() as conn:
            rows = await conn.fetch(query, limit, skip)
            return [dict(row) for row in rows]
    
    async def update(self, company_id: int, company_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a company."""
        set_clauses = []
        values = []
        param_count = 1
        
        for key, value in company_data.items():
            if value is not None:
                set_clauses.append(f"{key} = ${param_count}")
                values.append(value)
                param_count += 1
        
        if not set_clauses:
            return await self.get_by_id(company_id)
        
        values.append(company_id)
        query = f"""
            UPDATE companies 
            SET {', '.join(set_clauses)}
            WHERE id = ${param_count}
            RETURNING id, name, tax_code, email, address
        """
        
        async with get_pool().acquire() as conn:
            row = await conn.fetchrow(query, *values)
            return dict(row) if row else None
    
    async def delete(self, company_id: int) -> bool:
        """Delete a company."""
        query = "DELETE FROM companies WHERE id = $1 RETURNING id"
        async with get_pool().acquire() as conn:
            row = await conn.fetchrow(query, company_id)
            return row is not None
    
    async def get_monthly_costs(self, company_id: int, month: int, year: int) -> Dict[str, Any]:
        """
        Get company's monthly costs including rent and services.
        
        Returns:
            Dict with rent_cost, service_costs (list), total_cost
        """
        # Get rent cost for the month
        rent_query = """
            SELECT 
                SUM(rc.rent_price) as rent_cost,
                SUM(o.area) as total_area
            FROM rent_contracts rc
            JOIN offices o ON rc.office_id = o.id
            WHERE rc.company_id = $1
            AND rc.status = 'active'
            AND DATE_PART('year', rc.from_date) <= $2
            AND DATE_PART('month', rc.from_date) <= $3
            AND (rc.end_date IS NULL OR (
                DATE_PART('year', rc.end_date) >= $2
                AND DATE_PART('month', rc.end_date) >= $3
            ))
        """
        
        # Get monthly service costs
        service_query = """
            SELECT 
                s.name as service_name,
                SUM(cmu.price) as service_cost
            FROM company_monthly_usages cmu
            JOIN services s ON cmu.service_id = s.id
            WHERE cmu.company_id = $1
            AND DATE_PART('year', cmu.from_date) = $2
            AND DATE_PART('month', cmu.from_date) = $3
            GROUP BY s.id, s.name
        """
        
        # Get daily service costs (parking, meals)
        daily_query = """
            SELECT 
                s.name as service_name,
                SUM(edu.price) as service_cost
            FROM employee_daily_usages edu
            JOIN company_employees ce ON edu.employee_id = ce.id
            JOIN services s ON edu.service_id = s.id
            WHERE ce.company_id = $1
            AND DATE_PART('year', edu.usage_date) = $2
            AND DATE_PART('month', edu.usage_date) = $3
            GROUP BY s.id, s.name
        """
        
        async with get_pool().acquire() as conn:
            rent_row = await conn.fetchrow(rent_query, company_id, year, month)
            service_rows = await conn.fetch(service_query, company_id, year, month)
            daily_rows = await conn.fetch(daily_query, company_id, year, month)
            
            rent_cost = rent_row["rent_cost"] or 0
            total_area = rent_row["total_area"] or 0
            
            service_costs = [dict(row) for row in service_rows]
            service_costs.extend([dict(row) for row in daily_rows])
            
            total_service_cost = sum(item["service_cost"] or 0 for item in service_costs)
            total_cost = rent_cost + total_service_cost
            
            return {
                "company_id": company_id,
                "month": month,
                "year": year,
                "rent_cost": float(rent_cost),
                "total_area": float(total_area),
                "service_costs": service_costs,
                "total_service_cost": float(total_service_cost),
                "total_cost": float(total_cost)
            }
    
    async def get_service_details(self, company_id: int, month: int, year: int) -> dict:
        """Get detailed service usage and costs for a company."""
        async with get_pool().acquire() as conn:
            # Get company name
            company_row = await conn.fetchrow("SELECT name FROM companies WHERE id = $1", company_id)
            company_name = company_row['name'] if company_row else f"Company {company_id}"
            
            # Monthly services
            monthly_rows = await conn.fetch("""
                SELECT 
                    s.name as service_name,
                    cmu.quantity,
                    cmu.price,
                    (cmu.quantity * cmu.price) as total_cost
                FROM company_monthly_usages cmu
                JOIN services s ON cmu.service_id = s.id
                WHERE cmu.company_id = $1
                AND EXTRACT(YEAR FROM cmu.from_date) = $2
                AND EXTRACT(MONTH FROM cmu.from_date) = $3
            """, company_id, year, month)
            
            # Daily services
            daily_rows = await conn.fetch("""
                SELECT 
                    ce.full_name as employee_name,
                    s.name as service_name,
                    edu.usage_date,
                    edu.price
                FROM employee_daily_usages edu
                JOIN company_employees ce ON edu.employee_id = ce.id
                JOIN services s ON edu.service_id = s.id
                WHERE ce.company_id = $1
                AND EXTRACT(YEAR FROM edu.usage_date) = $2
                AND EXTRACT(MONTH FROM edu.usage_date) = $3
            """, company_id, year, month)
            
            monthly_total = sum(float(row['total_cost']) for row in monthly_rows)
            daily_total = sum(float(row['price']) for row in daily_rows)
            
            return {
                "company_id": company_id,
                "company_name": company_name,
                "month": month,
                "year": year,
                "monthly_services": [
                    {
                        "service_name": row["service_name"],
                        "quantity": float(row["quantity"]),
                        "unit_price": float(row["price"]),
                        "total_cost": float(row["total_cost"])
                    }
                    for row in monthly_rows
                ],
                "daily_services": [
                    {
                        "employee_name": row["employee_name"],
                        "service_name": row["service_name"],
                        "usage_date": row["usage_date"].isoformat(),
                        "price": float(row["price"])
                    }
                    for row in daily_rows
                ],
                "total_service_cost": monthly_total + daily_total
            }
