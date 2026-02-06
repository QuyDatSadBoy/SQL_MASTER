#!/usr/bin/env python3
"""
Script to reset database: Drop all tables and recreate schema
100% SQL thuần
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from auto_test.sql.db_utils import DatabaseUtils


async def reset_database():
    """Reset database by dropping and recreating."""
    db = DatabaseUtils()
    
    print("🔄 Resetting database...")
    
    try:
        await db.reset_database()
        print("✅ Database reset complete!")
        return True
    except Exception as e:
        print(f"❌ Error resetting database: {e}")
        return False
    finally:
        await db.close()


if __name__ == "__main__":
    success = asyncio.run(reset_database())
    sys.exit(0 if success else 1)
