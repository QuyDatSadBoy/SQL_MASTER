#!/usr/bin/env python3
"""
Script to truncate all tables (clear data but keep schema)
100% SQL thuần
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from auto_test.sql.db_utils import DatabaseUtils


async def truncate_all():
    """Truncate all tables."""
    db = DatabaseUtils()
    
    print("🔄 Truncating all tables...")
    
    try:
        await db.truncate_all_tables()
        
        # Verify
        tables = await db.get_table_names()
        print(f"\n📊 Tables after truncate:")
        for table in tables:
            count = await db.get_table_count(table)
            print(f"  • {table}: {count} rows")
        
        print("\n✅ Truncate complete!")
        return True
    except Exception as e:
        print(f"❌ Error truncating tables: {e}")
        return False
    finally:
        await db.close()


if __name__ == "__main__":
    success = asyncio.run(truncate_all())
    sys.exit(0 if success else 1)
