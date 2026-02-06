#!/usr/bin/env python3
"""
Script to test database connection
100% SQL thuần
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from auto_test.sql.db_utils import DatabaseUtils


async def test_connection():
    """Test database connection and show info."""
    db = DatabaseUtils()
    
    print("=" * 60)
    print("🔍 TESTING DATABASE CONNECTION")
    print("=" * 60)
    
    print(f"\n📌 Connection Info:")
    print(f"  Host: {db.host}")
    print(f"  Port: {db.port}")
    print(f"  User: {db.user}")
    print(f"  Database: {db.database}")
    
    try:
        # Test connection
        print(f"\n🔄 Testing connection...")
        if await db.test_connection():
            print("✅ Connection successful!")
            
            # Get database info
            version = await db.fetchval("SELECT version()")
            print(f"\n📊 PostgreSQL Version:")
            print(f"  {version}")
            
            # Get tables
            tables = await db.get_table_names()
            print(f"\n📋 Tables in database: {len(tables)}")
            
            if tables:
                for table in tables:
                    count = await db.get_table_count(table)
                    print(f"  • {table}: {count} rows")
            else:
                print("  ⚠️  No tables found. Run migrations first!")
            
            print("\n" + "=" * 60)
            print("✅ TEST COMPLETE")
            print("=" * 60)
            return True
        else:
            print("❌ Connection failed!")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        await db.close()


if __name__ == "__main__":
    success = asyncio.run(test_connection())
    sys.exit(0 if success else 1)
