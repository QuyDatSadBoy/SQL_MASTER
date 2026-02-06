"""
Database connection module using asyncpg.
Provides connection pool management for PostgreSQL.
"""
import asyncpg
from typing import Optional
from api.config import settings


# Global connection pool
_pool: Optional[asyncpg.Pool] = None


async def create_pool() -> asyncpg.Pool:
    """
    Create and return a connection pool.
    
    Returns:
        asyncpg.Pool: Database connection pool
    """
    global _pool
    
    _pool = await asyncpg.create_pool(
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        database=settings.POSTGRES_DB,
        min_size=5,
        max_size=20,
        command_timeout=60
    )
    
    return _pool


async def close_pool() -> None:
    """Close the database connection pool."""
    global _pool
    
    if _pool:
        await _pool.close()
        _pool = None


def get_pool() -> asyncpg.Pool:
    """
    Get the global connection pool.
    
    Returns:
        asyncpg.Pool: Database connection pool
        
    Raises:
        RuntimeError: If pool is not initialized
    """
    if _pool is None:
        raise RuntimeError("Database pool is not initialized. Call create_pool() first.")
    
    return _pool
