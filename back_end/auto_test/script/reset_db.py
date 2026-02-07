#!/usr/bin/env python3
"""
Script to reset database: xóa toàn bộ schema public rồi chạy lại migrations.
Không cần tắt server (uvicorn) — reset xóa tables/functions trong DB, không drop DB.
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from auto_test.sql.db_utils import DatabaseUtils


async def reset_database():
    """Reset: DROP SCHEMA public CASCADE + chạy lại migrations."""
    db = DatabaseUtils()
    migrations_dir = os.path.join(os.path.dirname(__file__), '../../migrations')
    migration_files = [
        '001_initial_schema.sql',
        '002_sample_data.sql',
        '003_building_employee_salary_function.sql',
        '004_report_functions.sql',
    ]

    try:
        print("Resetting database (DROP SCHEMA public CASCADE)...")
        await db.reset_database()
        print("Running migrations...")
        for filename in migration_files:
            filepath = os.path.join(migrations_dir, filename)
            if not os.path.exists(filepath):
                print(f"  [WARN] Not found: {filename}")
                continue
            print(f"  Executing: {filename}")
            await db.execute_file(filepath)
        print("Database reset and migrations complete.")
        return True
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        await db.close()


if __name__ == "__main__":
    success = asyncio.run(reset_database())
    sys.exit(0 if success else 1)
