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
        Lấy lương nhân viên tòa nhà theo tháng bằng function PostgreSQL.
        Lương = base_salary + sum(doanh thu dịch vụ × bonus_rate).
        """
        query = "SELECT * FROM get_building_employee_salaries($1, $2)"
        async with get_pool().acquire() as conn:
            rows = await conn.fetch(query, year, month)
            return [dict(row) for row in rows]
