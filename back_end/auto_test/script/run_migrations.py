#!/usr/bin/env python3
"""
Script to run database migrations
100% SQL thuần
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from auto_test.sql.db_utils import DatabaseUtils


async def run_migrations():
    """Run all migration files."""
    db = DatabaseUtils()
    
    migrations_dir = os.path.join(os.path.dirname(__file__), '../../migrations')
    migration_files = [
        '001_initial_schema.sql',
        '002_sample_data.sql'
    ]
    
    print("🔄 Running migrations...")
    
    try:
        for filename in migration_files:
            filepath = os.path.join(migrations_dir, filename)
            
            if not os.path.exists(filepath):
                print(f"⚠️  Migration file not found: {filename}")
                continue
            
            print(f"📄 Executing: {filename}")
            await db.execute_file(filepath)
            print(f"✅ Completed: {filename}")
        
        # Verify tables
        tables = await db.get_table_names()
        print(f"\n✅ Migration complete! Tables created: {len(tables)}")
        print(f"📊 Tables: {', '.join(tables)}")
        
        return True
    except Exception as e:
        print(f"❌ Error running migrations: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        await db.close()


if __name__ == "__main__":
    success = asyncio.run(run_migrations())
    sys.exit(0 if success else 1)
