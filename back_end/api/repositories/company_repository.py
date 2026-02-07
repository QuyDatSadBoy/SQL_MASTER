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
        Chi phí tháng của công ty (tiền thuê + dịch vụ) — gọi function PostgreSQL.
        """
        query = "SELECT * FROM get_company_monthly_costs($1, $2, $3)"
        async with get_pool().acquire() as conn:
            row = await conn.fetchrow(query, company_id, year, month)
            if not row:
                return {
                    "company_id": company_id,
                    "month": month,
                    "year": year,
                    "rent_cost": 0.0,
                    "total_area": 0.0,
                    "service_costs": [],
                    "total_service_cost": 0.0,
                    "total_cost": 0.0,
                }
            return {
                "company_id": row["company_id"],
                "month": row["month"],
                "year": row["year"],
                "rent_cost": float(row["rent_cost"] or 0),
                "total_area": float(row["total_area"] or 0),
                "service_costs": row["service_costs"] or [],
                "total_service_cost": float(row["total_service_cost"] or 0),
                "total_cost": float(row["total_cost"] or 0),
            }
    
    async def get_service_details(self, company_id: int, month: int, year: int) -> dict:
        """Chi tiết dịch vụ công ty theo tháng — gọi function PostgreSQL."""
        query = "SELECT * FROM get_company_service_details($1, $2, $3)"
        async with get_pool().acquire() as conn:
            row = await conn.fetchrow(query, company_id, year, month)
            if not row:
                return {
                    "company_id": company_id,
                    "company_name": "",
                    "month": month,
                    "year": year,
                    "monthly_services": [],
                    "daily_services": [],
                    "total_service_cost": 0.0,
                }
            monthly = row["monthly_services"] or []
            daily = row["daily_services"] or []
            if isinstance(daily, list):
                for d in daily:
                    if isinstance(d, dict) and "usage_date" in d:
                        ud = d["usage_date"]
                        if hasattr(ud, "isoformat"):
                            d["usage_date"] = ud.isoformat()
            return {
                "company_id": row["company_id"],
                "company_name": row["company_name"] or "",
                "month": row["month"],
                "year": row["year"],
                "monthly_services": monthly,
                "daily_services": daily,
                "total_service_cost": float(row["total_service_cost"] or 0),
            }
