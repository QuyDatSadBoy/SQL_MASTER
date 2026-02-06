"""
Repository for BuildingEmployee entity.
All database operations use raw SQL with asyncpg.
"""
from typing import List, Optional, Dict, Any
from api.database import get_pool


class BuildingEmployeeRepository:
    """Repository for BuildingEmployee CRUD operations."""
    
    async def create(self, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new building employee."""
        query = """
            INSERT INTO building_employees 
                (first_name, last_name, phone_number, role, email, address, 
                 date_of_birth, base_salary, hire_date, status)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            RETURNING employee_id, first_name, last_name, phone_number, role, 
                      email, address, date_of_birth, base_salary, hire_date, status
        """
        async with get_pool().acquire() as conn:
            row = await conn.fetchrow(
                query,
                employee_data.get("first_name"),
                employee_data.get("last_name"),
                employee_data.get("phone_number"),
                employee_data["role"],
                employee_data.get("email"),
                employee_data.get("address"),
                employee_data.get("date_of_birth"),
                employee_data.get("base_salary"),
                employee_data.get("hire_date"),
                employee_data.get("status")
            )
            return dict(row)
    
    async def get_by_id(self, employee_id: int) -> Optional[Dict[str, Any]]:
        """Get employee by ID."""
        query = "SELECT * FROM building_employees WHERE employee_id = $1"
        async with get_pool().acquire() as conn:
            row = await conn.fetchrow(query, employee_id)
            return dict(row) if row else None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all employees with pagination."""
        query = "SELECT * FROM building_employees ORDER BY employee_id LIMIT $1 OFFSET $2"
        async with get_pool().acquire() as conn:
            rows = await conn.fetch(query, limit, skip)
            return [dict(row) for row in rows]
    
    async def update(self, employee_id: int, employee_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an employee."""
        set_clauses = []
        values = []
        param_count = 1
        
        for key, value in employee_data.items():
            if value is not None:
                set_clauses.append(f"{key} = ${param_count}")
                values.append(value)
                param_count += 1
        
        if not set_clauses:
            return await self.get_by_id(employee_id)
        
        values.append(employee_id)
        query = f"""
            UPDATE building_employees 
            SET {', '.join(set_clauses)}
            WHERE employee_id = ${param_count}
            RETURNING *
        """
        
        async with get_pool().acquire() as conn:
            row = await conn.fetchrow(query, *values)
            return dict(row) if row else None
    
    async def delete(self, employee_id: int) -> bool:
        """Delete an employee."""
        query = "DELETE FROM building_employees WHERE employee_id = $1 RETURNING employee_id"
        async with get_pool().acquire() as conn:
            row = await conn.fetchrow(query, employee_id)
            return row is not None
    
    async def get_salaries(self, month: int, year: int) -> List[Dict[str, Any]]:
        """
        Calculate salaries for building employees for a specific month.
        Salary = base_salary + (revenue * bonus_rate)
        """
        query = """
            SELECT 
                be.employee_id,
                CONCAT(be.first_name, ' ', be.last_name) as full_name,
                be.role,
                be.base_salary,
                COALESCE(sr.bonus_rate, 0) as bonus_rate,
                COALESCE(SUM(cmu.price), 0) as monthly_revenue,
                be.base_salary + (COALESCE(SUM(cmu.price), 0) * COALESCE(sr.bonus_rate, 0)) as total_salary
            FROM building_employees be
            LEFT JOIN service_subscribers ss ON be.employee_id = ss.employee_id
                AND ss.from_date <= MAKE_DATE($1, $2, 1) + INTERVAL '1 month' - INTERVAL '1 day'
                AND (ss.end_date IS NULL OR ss.end_date >= MAKE_DATE($1, $2, 1))
            LEFT JOIN service_role_rules srr ON ss.service_role_rules_id = srr.id
            LEFT JOIN salary_rules sr ON srr.salary_rule_id = sr.id
            LEFT JOIN company_monthly_usages cmu ON cmu.service_id = srr.service_id
                AND EXTRACT(YEAR FROM cmu.from_date) = $1
                AND EXTRACT(MONTH FROM cmu.from_date) = $2
            GROUP BY be.employee_id, be.first_name, be.last_name, be.role, 
                     be.base_salary, sr.bonus_rate
            ORDER BY be.employee_id
        """
        
        async with get_pool().acquire() as conn:
            rows = await conn.fetch(query, year, month)
            return [dict(row) for row in rows]
