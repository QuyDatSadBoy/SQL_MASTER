"""
SQL Database Utilities for Auto Testing
100% SQL thuần - KHÔNG dùng ORM
"""
import asyncpg
import os
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class DatabaseUtils:
    """Utility class for database operations using pure SQL."""
    
    def __init__(self, use_test_db: bool = False):
        """
        Initialize database utilities.
        
        Args:
            use_test_db: If True, connect to test database
        """
        self.host = os.getenv("POSTGRES_HOST", "localhost")
        self.port = int(os.getenv("POSTGRES_PORT", "5432"))
        self.user = os.getenv("POSTGRES_USER", "postgres")
        self.password = os.getenv("POSTGRES_PASSWORD", "")
        
        if use_test_db:
            self.database = os.getenv("TEST_DB_NAME", "office_db_test")
        else:
            self.database = os.getenv("POSTGRES_DB", "office_db")
        
        self._connection: Optional[asyncpg.Connection] = None
    
    async def connect(self) -> asyncpg.Connection:
        """
        Establish database connection.
        
        Returns:
            asyncpg.Connection: Database connection
        """
        if self._connection is None or self._connection.is_closed():
            self._connection = await asyncpg.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
        return self._connection
    
    async def close(self):
        """Close database connection."""
        if self._connection and not self._connection.is_closed():
            await self._connection.close()
            self._connection = None
    
    async def execute(self, query: str, *args) -> str:
        """
        Execute a SQL query (INSERT, UPDATE, DELETE).
        
        Args:
            query: SQL query string
            *args: Query parameters
        
        Returns:
            str: Execution status
        """
        conn = await self.connect()
        result = await conn.execute(query, *args)
        return result
    
    async def fetchone(self, query: str, *args) -> Optional[Dict[str, Any]]:
        """
        Fetch one row from database.
        
        Args:
            query: SQL query string
            *args: Query parameters
        
        Returns:
            dict: Row as dictionary or None
        """
        conn = await self.connect()
        row = await conn.fetchrow(query, *args)
        return dict(row) if row else None
    
    async def fetchall(self, query: str, *args) -> List[Dict[str, Any]]:
        """
        Fetch all rows from database.
        
        Args:
            query: SQL query string
            *args: Query parameters
        
        Returns:
            list: List of rows as dictionaries
        """
        conn = await self.connect()
        rows = await conn.fetch(query, *args)
        return [dict(row) for row in rows]
    
    async def fetchval(self, query: str, *args) -> Any:
        """
        Fetch a single value.
        
        Args:
            query: SQL query string
            *args: Query parameters
        
        Returns:
            Any: Single value
        """
        conn = await self.connect()
        return await conn.fetchval(query, *args)
    
    async def execute_script(self, script: str):
        """
        Execute a SQL script (multiple statements).
        
        Args:
            script: SQL script content
        """
        conn = await self.connect()
        await conn.execute(script)
    
    async def execute_file(self, filepath: str):
        """
        Execute SQL commands from a file.
        
        Args:
            filepath: Path to SQL file
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            script = f.read()
        await self.execute_script(script)
    
    async def test_connection(self) -> bool:
        """
        Test database connection.
        
        Returns:
            bool: True if connection successful
        """
        try:
            conn = await self.connect()
            result = await conn.fetchval("SELECT 1")
            return result == 1
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    async def database_exists(self, db_name: str) -> bool:
        """
        Check if database exists.
        
        Args:
            db_name: Database name
        
        Returns:
            bool: True if exists
        """
        # Connect to postgres database to check
        conn = await asyncpg.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database="postgres"
        )
        
        query = "SELECT 1 FROM pg_database WHERE datname = $1"
        exists = await conn.fetchval(query, db_name)
        await conn.close()
        
        return exists == 1
    
    async def create_database(self, db_name: str):
        """
        Create database (SQL thuần).
        
        Args:
            db_name: Database name
        """
        conn = await asyncpg.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database="postgres"
        )
        
        await conn.execute(f'CREATE DATABASE "{db_name}"')
        await conn.close()
        print(f"✅ Database '{db_name}' created")
    
    async def drop_database(self, db_name: str):
        """
        Drop database (SQL thuần).
        
        Args:
            db_name: Database name
        """
        conn = await asyncpg.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database="postgres"
        )
        
        # Terminate all connections to the database first
        await conn.execute(f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{db_name}'
            AND pid <> pg_backend_pid()
        """)
        
        await conn.execute(f'DROP DATABASE IF EXISTS "{db_name}"')
        await conn.close()
        print(f"✅ Database '{db_name}' dropped")
    
    async def reset_database(self):
        """Drop and recreate current database."""
        db_name = self.database
        await self.close()
        
        # Drop and create
        await self.drop_database(db_name)
        await self.create_database(db_name)
    
    async def get_table_names(self) -> List[str]:
        """
        Get all table names in current database.
        
        Returns:
            list: List of table names
        """
        query = """
            SELECT tablename 
            FROM pg_tables 
            WHERE schemaname = 'public'
            ORDER BY tablename
        """
        rows = await self.fetchall(query)
        return [row['tablename'] for row in rows]
    
    async def get_table_count(self, table_name: str) -> int:
        """
        Get row count of a table.
        
        Args:
            table_name: Table name
        
        Returns:
            int: Row count
        """
        query = f"SELECT COUNT(*) FROM {table_name}"
        return await self.fetchval(query)
    
    async def truncate_all_tables(self):
        """Truncate all tables (cascade)."""
        tables = await self.get_table_names()
        
        if tables:
            tables_str = ", ".join(tables)
            query = f"TRUNCATE TABLE {tables_str} RESTART IDENTITY CASCADE"
            await self.execute(query)
            print(f"✅ Truncated {len(tables)} tables")


# Quick access functions for convenience
async def quick_query(query: str, *args, use_test_db: bool = False) -> List[Dict[str, Any]]:
    """
    Quick query execution (returns all rows).
    
    Usage:
        results = await quick_query("SELECT * FROM offices WHERE floor = $1", 1)
    """
    db = DatabaseUtils(use_test_db=use_test_db)
    try:
        return await db.fetchall(query, *args)
    finally:
        await db.close()


async def quick_execute(query: str, *args, use_test_db: bool = False) -> str:
    """
    Quick execution (INSERT, UPDATE, DELETE).
    
    Usage:
        await quick_execute("DELETE FROM offices WHERE id = $1", 1)
    """
    db = DatabaseUtils(use_test_db=use_test_db)
    try:
        return await db.execute(query, *args)
    finally:
        await db.close()


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def main():
        db = DatabaseUtils()
        
        # Test connection
        if await db.test_connection():
            print("✅ Database connection successful!")
            
            # Get table names
            tables = await db.get_table_names()
            print(f"\n📊 Tables in database: {tables}")
            
            # Example query
            offices = await db.fetchall("SELECT * FROM offices LIMIT 5")
            print(f"\n🏢 First 5 offices: {len(offices)} records")
            
        await db.close()
    
    asyncio.run(main())
