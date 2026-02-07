#!/usr/bin/env python3
"""
Script to setup fresh database: Reset + Run migrations
100% SQL thuần
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from auto_test.sql.db_utils import DatabaseUtils


async def setup_database():
    """Setup fresh database with schema and data."""
    db = DatabaseUtils()
    
    print("=" * 60)
    print("🚀 SETTING UP FRESH DATABASE")
    print("=" * 60)
    
    try:
        # Step 1: Check if database exists
        db_name = db.database
        exists = await db.database_exists(db_name)
        
        if exists:
            print(f"\n🔄 Database '{db_name}' exists. Dropping...")
            await db.drop_database(db_name)
        
        # Step 2: Create database
        print(f"\n📦 Creating database '{db_name}'...")
        await db.create_database(db_name)
        
        # Step 3: Run migrations
        print("\n🔄 Running migrations...")
        migrations_dir = os.path.join(os.path.dirname(__file__), '../../migrations')
        migration_files = [
            '001_initial_schema.sql',
            '002_sample_data.sql',
            '003_building_employee_salary_function.sql',
            '004_report_functions.sql',
        ]
        
        # Need to reconnect after creating database
        await db.close()
        db = DatabaseUtils()
        
        for filename in migration_files:
            filepath = os.path.join(migrations_dir, filename)
            
            if not os.path.exists(filepath):
                print(f"⚠️  Migration file not found: {filename}")
                continue
            
            print(f"  📄 Executing: {filename}")
            await db.execute_file(filepath)
            print(f"  ✅ Completed: {filename}")
        
        # Step 4: Verify setup
        print("\n📊 Verifying database setup...")
        tables = await db.get_table_names()
        print(f"  ✅ Tables created: {len(tables)}")
        
        for table in tables:
            count = await db.get_table_count(table)
            print(f"    • {table}: {count} rows")
        
        print("\n" + "=" * 60)
        print("✅ DATABASE SETUP COMPLETE!")
        print("=" * 60)
        
        return True
    except Exception as e:
        print(f"\n❌ Error setting up database: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        await db.close()


if __name__ == "__main__":
    success = asyncio.run(setup_database())
    sys.exit(0 if success else 1)
