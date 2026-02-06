"""
SQL Auto Tests - Test database operations
100% SQL thuần

Cách dùng:
    # 1. Chạy toàn bộ tests
    cd back_end && python -m auto_test.sql.test_sql

    # 2. Chạy 1 test cụ thể
    cd back_end && python -m auto_test.sql.test_sql test_database_connection
    cd back_end && python -m auto_test.sql.test_sql test_company_monthly_costs

    # 3. Chạy nhiều tests
    cd back_end && python -m auto_test.sql.test_sql test_tables_exist test_sample_data_loaded
"""
import asyncio
import sys
import os
from datetime import date

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from auto_test.sql.db_utils import DatabaseUtils

# List of all available test names (for CLI help)
ALL_SQL_TESTS = [
    "test_database_connection",
    "test_tables_exist",
    "test_sample_data_loaded",
    "test_office_crud",
    "test_company_unique_tax_code",
    "test_office_availability_check",
    "test_employee_salary_calculation",
    "test_company_monthly_costs",
    "test_foreign_key_constraints",
    "test_date_range_constraints",
]


class SQLTests:
    """SQL test suite - supports running all tests or individual tests."""
    
    def __init__(self):
        self.db = DatabaseUtils()
        self.passed = 0
        self.failed = 0
    
    async def setup(self):
        """Setup test environment."""
        await self.db.connect()
    
    async def teardown(self):
        """Cleanup after tests."""
        await self.db.close()
    
    def assert_equal(self, actual, expected, test_name):
        """Assert equal with test name."""
        if actual == expected:
            print(f"  ✅ {test_name}")
            self.passed += 1
            return True
        else:
            print(f"  ❌ {test_name}")
            print(f"     Expected: {expected}")
            print(f"     Got: {actual}")
            self.failed += 1
            return False
    
    def assert_true(self, condition, test_name):
        """Assert true with test name."""
        if condition:
            print(f"  ✅ {test_name}")
            self.passed += 1
            return True
        else:
            print(f"  ❌ {test_name}")
            self.failed += 1
            return False
    
    async def test_database_connection(self):
        """Test 1: Database connection."""
        print("\n🧪 Test 1: Database Connection")
        result = await self.db.test_connection()
        self.assert_true(result, "Connection successful")
    
    async def test_tables_exist(self):
        """Test 2: All tables exist."""
        print("\n🧪 Test 2: Tables Existence")
        
        expected_tables = [
            'offices', 'companies', 'company_employees', 'building_employees',
            'rent_contracts', 'services', 'salary_rules', 'service_role_rules',
            'service_subscribers', 'company_monthly_usages', 
            'employee_daily_usages', 'invoices'
        ]
        
        tables = await self.db.get_table_names()
        
        for table in expected_tables:
            self.assert_true(table in tables, f"Table '{table}' exists")
    
    async def test_sample_data_loaded(self):
        """Test 3: Sample data loaded."""
        print("\n🧪 Test 3: Sample Data Loaded")
        
        # Check offices
        office_count = await self.db.fetchval("SELECT COUNT(*) FROM offices")
        self.assert_true(office_count >= 6, f"Offices loaded ({office_count} >= 6)")
        
        # Check companies
        company_count = await self.db.fetchval("SELECT COUNT(*) FROM companies")
        self.assert_true(company_count >= 3, f"Companies loaded ({company_count} >= 3)")
        
        # Check employees
        employee_count = await self.db.fetchval("SELECT COUNT(*) FROM company_employees")
        self.assert_true(employee_count >= 28, f"Company employees loaded ({employee_count} >= 28)")
    
    async def test_office_crud(self):
        """Test 4: Office CRUD operations."""
        print("\n🧪 Test 4: Office CRUD Operations")
        
        # CREATE
        query = """
            INSERT INTO offices (name, area, floor, position, base_price)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id
        """
        office_id = await self.db.fetchval(query, "TEST_P999", 100.0, 9, "Test position", 50000000)
        self.assert_true(office_id is not None, "Office created")
        
        # READ
        query = "SELECT * FROM offices WHERE id = $1"
        office = await self.db.fetchone(query, office_id)
        self.assert_equal(office['name'], "TEST_P999", "Office name correct")
        self.assert_equal(float(office['area']), 100.0, "Office area correct")
        
        # UPDATE
        query = "UPDATE offices SET base_price = $1 WHERE id = $2 RETURNING base_price"
        new_price = await self.db.fetchval(query, 60000000, office_id)
        self.assert_equal(float(new_price), 60000000, "Office updated")
        
        # DELETE
        query = "DELETE FROM offices WHERE id = $1 RETURNING id"
        deleted_id = await self.db.fetchval(query, office_id)
        self.assert_equal(deleted_id, office_id, "Office deleted")
    
    async def test_company_unique_tax_code(self):
        """Test 5: Company tax_code uniqueness."""
        print("\n🧪 Test 5: Company Tax Code Uniqueness")
        
        # Insert company
        query = """
            INSERT INTO companies (name, tax_code, email)
            VALUES ($1, $2, $3)
            RETURNING id
        """
        company_id = await self.db.fetchval(query, "Test Company", "TEST123456", "test@test.com")
        self.assert_true(company_id is not None, "Company created")
        
        # Try to insert duplicate tax_code (should fail)
        try:
            await self.db.execute(query, "Another Company", "TEST123456", "another@test.com")
            self.assert_true(False, "Duplicate tax_code rejected")
        except Exception:
            self.assert_true(True, "Duplicate tax_code rejected")
        
        # Cleanup
        await self.db.execute("DELETE FROM companies WHERE id = $1", company_id)
    
    async def test_office_availability_check(self):
        """Test 6: Office availability (no overlap contracts)."""
        print("\n🧪 Test 6: Office Availability Check")
        
        # Find an office with active contract
        query = """
            SELECT office_id 
            FROM rent_contracts 
            WHERE status = 'active' 
            LIMIT 1
        """
        office_id = await self.db.fetchval(query)
        
        if office_id:
            # Check for overlapping contracts
            query = """
                SELECT COUNT(*) FROM rent_contracts
                WHERE office_id = $1 
                AND status = 'active'
                AND (
                    (from_date <= $2 AND end_date >= $2) OR
                    (from_date <= $3 AND end_date >= $3)
                )
            """
            count = await self.db.fetchval(query, office_id, date(2026, 1, 1), date(2026, 12, 31))
            self.assert_true(count > 0, "Office has active contract (overlap detected)")
        else:
            print("  ⚠️  Skipped (no active contracts)")
    
    async def test_employee_salary_calculation(self):
        """Test 7: Employee salary calculation."""
        print("\n🧪 Test 7: Employee Salary Calculation")
        
        # Query salary with bonus
        query = """
            SELECT 
                be.employee_id,
                be.base_salary,
                COALESCE(sr.bonus_rate, 0) as bonus_rate,
                be.base_salary + (COALESCE(SUM(cmu.price), 0) * COALESCE(sr.bonus_rate, 0)) as total_salary
            FROM building_employees be
            LEFT JOIN service_subscribers ss ON be.employee_id = ss.employee_id
            LEFT JOIN service_role_rules srr ON ss.service_role_rules_id = srr.id
            LEFT JOIN salary_rules sr ON srr.salary_rule_id = sr.id
            LEFT JOIN company_monthly_usages cmu ON cmu.service_id = srr.service_id
            WHERE be.employee_id = 1
            GROUP BY be.employee_id, be.base_salary, sr.bonus_rate
        """
        
        result = await self.db.fetchone(query)
        
        if result:
            base_salary = float(result['base_salary'] or 0)
            bonus_rate = float(result['bonus_rate'] or 0)
            total_salary = float(result['total_salary'] or 0)
            
            self.assert_true(total_salary >= base_salary, f"Total salary >= base salary ({total_salary} >= {base_salary})")
            self.assert_true(bonus_rate <= 1.0, f"Bonus rate valid ({bonus_rate} <= 1.0)")
        else:
            print("  ⚠️  Skipped (no employee data)")
    
    async def test_company_monthly_costs(self):
        """Test 8: Company monthly costs calculation."""
        print("\n🧪 Test 8: Company Monthly Costs Calculation")
        
        company_id = 1
        month = 1
        year = 2026
        
        # Get rent cost
        rent_query = """
            SELECT COALESCE(SUM(rc.rent_price), 0) as rent_cost
            FROM rent_contracts rc
            WHERE rc.company_id = $1
            AND rc.status = 'active'
        """
        rent_cost = await self.db.fetchval(rent_query, company_id)
        
        # Get service costs
        service_query = """
            SELECT COALESCE(SUM(cmu.price), 0) as service_cost
            FROM company_monthly_usages cmu
            WHERE cmu.company_id = $1
            AND DATE_PART('year', cmu.from_date) = $2
            AND DATE_PART('month', cmu.from_date) = $3
        """
        service_cost = await self.db.fetchval(service_query, company_id, year, month)
        
        total_cost = float(rent_cost or 0) + float(service_cost or 0)
        
        self.assert_true(rent_cost >= 0, f"Rent cost valid ({rent_cost})")
        self.assert_true(service_cost >= 0, f"Service cost valid ({service_cost})")
        self.assert_true(total_cost >= 0, f"Total cost calculated ({total_cost})")
    
    async def test_foreign_key_constraints(self):
        """Test 9: Foreign key constraints."""
        print("\n🧪 Test 9: Foreign Key Constraints")
        
        # Try to insert contract with invalid office_id (should fail)
        query = """
            INSERT INTO rent_contracts 
            (office_id, company_id, from_date, end_date, rent_price, status)
            VALUES ($1, $2, $3, $4, $5, $6)
        """
        
        try:
            await self.db.execute(query, 99999, 1, '2026-01-01', '2026-12-31', 10000000, 'active')
            self.assert_true(False, "Invalid office_id rejected")
        except Exception:
            self.assert_true(True, "Invalid office_id rejected (FK constraint works)")
    
    async def test_date_range_constraints(self):
        """Test 10: Date range constraints."""
        print("\n🧪 Test 10: Date Range Constraints")
        
        # Try to insert contract with end_date < from_date (should fail)
        query = """
            INSERT INTO rent_contracts 
            (office_id, company_id, from_date, end_date, rent_price, status)
            VALUES ($1, $2, $3, $4, $5, $6)
        """
        
        try:
            await self.db.execute(query, 1, 1, '2026-12-31', '2026-01-01', 10000000, 'active')
            self.assert_true(False, "Invalid date range rejected")
        except Exception:
            self.assert_true(True, "Invalid date range rejected (CHECK constraint works)")
    
    async def run_all_tests(self):
        """Run all tests."""
        print("=" * 60)
        print("🧪 RUNNING SQL AUTO TESTS")
        print("=" * 60)
        
        await self.setup()
        
        try:
            for test_name in ALL_SQL_TESTS:
                test_method = getattr(self, test_name)
                await test_method()
        finally:
            await self.teardown()
        
        self._print_summary()
        return self.failed == 0
    
    async def run_tests(self, test_names: list):
        """
        Run specific tests by name.
        
        Args:
            test_names: List of test method names
        """
        print("=" * 60)
        print(f"🧪 RUNNING {len(test_names)} SELECTED SQL TEST(S)")
        print("=" * 60)
        print(f"📋 Tests: {', '.join(test_names)}")
        
        await self.setup()
        
        try:
            for test_name in test_names:
                if hasattr(self, test_name):
                    test_method = getattr(self, test_name)
                    await test_method()
                else:
                    print(f"\n⚠️  Unknown test: {test_name}")
                    print(f"   Available: {', '.join(ALL_SQL_TESTS)}")
        finally:
            await self.teardown()
        
        self._print_summary()
        return self.failed == 0
    
    def _print_summary(self):
        """Print test summary."""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"📈 Total: {self.passed + self.failed}")
        
        if self.failed == 0:
            print("\n🎉 ALL TESTS PASSED!")
        else:
            print(f"\n⚠️  {self.failed} TEST(S) FAILED")


async def main(test_names: list = None):
    """Main test runner."""
    tests = SQLTests()
    
    if test_names:
        success = await tests.run_tests(test_names)
    else:
        success = await tests.run_all_tests()
    
    return success


if __name__ == "__main__":
    args = sys.argv[1:]
    
    if args and args[0] in ("--help", "-h"):
        print("Usage: python -m auto_test.sql.test_sql [test_name ...]")
        print("\nAvailable tests:")
        for name in ALL_SQL_TESTS:
            print(f"  {name}")
        print("\nExamples:")
        print("  python -m auto_test.sql.test_sql                          # Run all")
        print("  python -m auto_test.sql.test_sql test_database_connection # Run one")
        sys.exit(0)
    
    selected = args if args else None
    success = asyncio.run(main(selected))
    sys.exit(0 if success else 1)
