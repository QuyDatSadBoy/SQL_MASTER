"""
Transaction management module.
Provides context manager for database transactions.
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import asyncpg
from api.database.connection import get_pool


@asynccontextmanager
async def transaction() -> AsyncGenerator[asyncpg.Connection, None]:
    """
    Context manager for database transactions.
    
    Usage:
        async with transaction() as conn:
            await conn.execute("INSERT INTO ...")
            await conn.execute("UPDATE ...")
    
    Yields:
        asyncpg.Connection: Database connection with active transaction
    """
    pool = get_pool()
    async with pool.acquire() as conn:
        async with conn.transaction():
            yield conn
