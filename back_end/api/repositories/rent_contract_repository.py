"""
Repository for RentContract entity.
All database operations use raw SQL with asyncpg.
"""
from typing import List, Optional, Dict, Any
from api.database import get_pool


class RentContractRepository:
    """Repository for RentContract CRUD operations."""
    
    async def create(self, contract_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new rent contract."""
        query = """
            INSERT INTO rent_contracts 
                (office_id, company_id, invoice_id, from_date, end_date, 
                 signed_date, rent_price, status)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            RETURNING id, office_id, company_id, invoice_id, from_date, 
                      end_date, signed_date, rent_price, status
        """
        async with get_pool().acquire() as conn:
            row = await conn.fetchrow(
                query,
                contract_data["office_id"],
                contract_data["company_id"],
                contract_data.get("invoice_id"),
                contract_data["from_date"],
                contract_data["end_date"],
                contract_data.get("signed_date"),
                contract_data["rent_price"],
                contract_data.get("status", "active")
            )
            return dict(row)
    
    async def get_by_id(self, contract_id: int) -> Optional[Dict[str, Any]]:
        """Get contract by ID."""
        query = "SELECT * FROM rent_contracts WHERE id = $1"
        async with get_pool().acquire() as conn:
            row = await conn.fetchrow(query, contract_id)
            return dict(row) if row else None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all contracts with pagination."""
        query = "SELECT * FROM rent_contracts ORDER BY id LIMIT $1 OFFSET $2"
        async with get_pool().acquire() as conn:
            rows = await conn.fetch(query, limit, skip)
            return [dict(row) for row in rows]
    
    async def get_by_company(self, company_id: int) -> List[Dict[str, Any]]:
        """Get all contracts for a company."""
        query = """
            SELECT * FROM rent_contracts 
            WHERE company_id = $1 
            ORDER BY from_date DESC
        """
        async with get_pool().acquire() as conn:
            rows = await conn.fetch(query, company_id)
            return [dict(row) for row in rows]

    async def get_by_company_with_office(self, company_id: int) -> List[Dict[str, Any]]:
        """Get all contracts for a company, kèm tên và diện tích văn phòng."""
        query = """
            SELECT rc.id, rc.office_id, rc.company_id, rc.invoice_id,
                   rc.from_date, rc.end_date, rc.signed_date, rc.rent_price, rc.status,
                   o.name AS office_name, o.area AS office_area
            FROM rent_contracts rc
            JOIN offices o ON rc.office_id = o.id
            WHERE rc.company_id = $1
            ORDER BY rc.from_date DESC
        """
        async with get_pool().acquire() as conn:
            rows = await conn.fetch(query, company_id)
            return [dict(row) for row in rows]
    
    async def update(self, contract_id: int, contract_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a contract."""
        set_clauses = []
        values = []
        param_count = 1
        
        for key, value in contract_data.items():
            if value is not None:
                set_clauses.append(f"{key} = ${param_count}")
                values.append(value)
                param_count += 1
        
        if not set_clauses:
            return await self.get_by_id(contract_id)
        
        values.append(contract_id)
        query = f"""
            UPDATE rent_contracts 
            SET {', '.join(set_clauses)}
            WHERE id = ${param_count}
            RETURNING *
        """
        
        async with get_pool().acquire() as conn:
            row = await conn.fetchrow(query, *values)
            return dict(row) if row else None
    
    async def delete(self, contract_id: int) -> bool:
        """Delete a contract."""
        query = "DELETE FROM rent_contracts WHERE id = $1 RETURNING id"
        async with get_pool().acquire() as conn:
            row = await conn.fetchrow(query, contract_id)
            return row is not None
