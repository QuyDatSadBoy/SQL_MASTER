"""
Repository for Office entity.
All database operations use raw SQL with asyncpg.
"""
from typing import List, Optional, Dict, Any
from api.database import get_pool


class OfficeRepository:
    """Repository for Office CRUD operations."""
    
    async def create(self, office_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new office."""
        query = """
            INSERT INTO offices (name, area, floor, position, base_price)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id, name, area, floor, position, base_price
        """
        async with get_pool().acquire() as conn:
            row = await conn.fetchrow(
                query,
                office_data["name"],
                office_data["area"],
                office_data["floor"],
                office_data.get("position"),
                office_data["base_price"]
            )
            return dict(row)
    
    async def get_by_id(self, office_id: int) -> Optional[Dict[str, Any]]:
        """Get office by ID."""
        query = "SELECT * FROM offices WHERE id = $1"
        async with get_pool().acquire() as conn:
            row = await conn.fetchrow(query, office_id)
            return dict(row) if row else None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all offices with pagination."""
        query = "SELECT * FROM offices ORDER BY id LIMIT $1 OFFSET $2"
        async with get_pool().acquire() as conn:
            rows = await conn.fetch(query, limit, skip)
            return [dict(row) for row in rows]
    
    async def update(self, office_id: int, office_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an office."""
        # Build dynamic update query
        set_clauses = []
        values = []
        param_count = 1
        
        for key, value in office_data.items():
            if value is not None:
                set_clauses.append(f"{key} = ${param_count}")
                values.append(value)
                param_count += 1
        
        if not set_clauses:
            return await self.get_by_id(office_id)
        
        values.append(office_id)
        query = f"""
            UPDATE offices 
            SET {', '.join(set_clauses)}
            WHERE id = ${param_count}
            RETURNING id, name, area, floor, position, base_price
        """
        
        async with get_pool().acquire() as conn:
            row = await conn.fetchrow(query, *values)
            return dict(row) if row else None
    
    async def delete(self, office_id: int) -> bool:
        """Delete an office."""
        query = "DELETE FROM offices WHERE id = $1 RETURNING id"
        async with get_pool().acquire() as conn:
            row = await conn.fetchrow(query, office_id)
            return row is not None
    
    async def check_availability(
        self, 
        office_id: int, 
        from_date: str, 
        to_date: str,
        exclude_contract_id: Optional[int] = None
    ) -> bool:
        """
        Check if office is available for rent in the given date range.
        Returns True if available, False if already rented.
        """
        query = """
            SELECT COUNT(*) as count FROM rent_contracts
            WHERE office_id = $1 
            AND status = 'active'
            AND (
                (from_date <= $2 AND end_date >= $2) OR
                (from_date <= $3 AND end_date >= $3) OR
                (from_date >= $2 AND end_date <= $3)
            )
        """
        
        params = [office_id, from_date, to_date]
        
        # Exclude current contract when updating
        if exclude_contract_id:
            query += " AND id != $4"
            params.append(exclude_contract_id)
        
        async with get_pool().acquire() as conn:
            row = await conn.fetchrow(query, *params)
            return row["count"] == 0
