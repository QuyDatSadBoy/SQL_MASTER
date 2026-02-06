"""
API Auto Tests - Test FastAPI endpoints
100% SQL thuần (backend uses raw SQL)

Cách dùng:
    # 1. Chạy toàn bộ tests
    cd back_end && python -m auto_test.api.test_api

    # 2. Chạy 1 test cụ thể
    cd back_end && python -m auto_test.api.test_api test_health_check
    cd back_end && python -m auto_test.api.test_api test_company_monthly_costs

    # 3. Chạy nhiều tests
    cd back_end && python -m auto_test.api.test_api test_health_check test_list_offices

    # 4. Import và chạy trong code
    from auto_test.api.test_api import APITests
    tests = APITests()
    await tests.setup()
    await tests.test_company_monthly_costs()
    await tests.teardown()
"""
import asyncio
import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import httpx
from dotenv import load_dotenv

load_dotenv()

# List of all available test names (for CLI help)
ALL_TESTS = [
    "test_health_check",
    "test_list_offices",
    "test_create_office",
    "test_get_office",
    "test_update_office",
    "test_delete_office",
    "test_list_companies",
    "test_create_company",
    "test_company_monthly_costs",
    "test_list_contracts",
    "test_list_building_employees",
    "test_employee_salaries",
    "test_pagination",
    "test_invalid_id",
    "test_validation_errors",
    "test_company_service_details",
    "test_building_finance",
    "test_building_finance_details",
]


class APITests:
    """API test suite - supports running all tests or individual tests."""

    def __init__(self):
        port = os.getenv("APP_PORT", "8222")
        self.base_url = f"http://localhost:{port}/api"
        self.client = None
        self.passed = 0
        self.failed = 0

    def assert_status(self, response, expected_status, test_name):
        """Assert response status code."""
        if response.status_code == expected_status:
            print(f"  ✅ {test_name} (status: {response.status_code})")
            self.passed += 1
            return True
        else:
            print(f"  ❌ {test_name}")
            print(f"     Expected status: {expected_status}")
            print(f"     Got status: {response.status_code}")
            print(f"     Response: {response.text[:200]}")
            self.failed += 1
            return False

    def assert_true(self, condition, test_name, message=""):
        """Assert condition is true."""
        if condition:
            print(f"  ✅ {test_name}")
            self.passed += 1
            return True
        else:
            print(f"  ❌ {test_name}")
            if message:
                print(f"     {message}")
            self.failed += 1
            return False
    
    async def setup(self):
        """Setup test client."""
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def teardown(self):
        """Cleanup after tests."""
        if self.client:
            await self.client.aclose()
    
    async def test_health_check(self):
        """Test 1: Health check endpoint."""
        print("\n🧪 Test 1: Health Check")
        
        response = await self.client.get(f"http://localhost:{os.getenv('APP_PORT', '8222')}/health")
        self.assert_status(response, 200, "Health check returns 200")
        
        if response.status_code == 200:
            data = response.json()
            self.assert_true("status" in data, "Response has 'status' field")
    
    async def test_list_offices(self):
        """Test 2: List offices."""
        print("\n🧪 Test 2: List Offices")
        
        response = await self.client.get(f"{self.base_url}/offices")
        self.assert_status(response, 200, "List offices returns 200")
        
        if response.status_code == 200:
            data = response.json()
            self.assert_true(isinstance(data, list), "Response is a list")
            self.assert_true(len(data) > 0, f"Has offices ({len(data)} offices)")
    
    async def test_create_office(self):
        """Test 3: Create office."""
        print("\n🧪 Test 3: Create Office")
        
        office_data = {
            "name": "TEST_API_P888",
            "area": 85.50,
            "floor": 8,
            "position": "Test API Position",
            "base_price": 28000000
        }
        
        response = await self.client.post(f"{self.base_url}/offices", json=office_data)
        self.assert_status(response, 201, "Create office returns 201")
        
        if response.status_code == 201:
            data = response.json()
            self.assert_true("id" in data, "Response has 'id' field")
            self.assert_true(data["name"] == office_data["name"], "Office name matches")
            
            # Cleanup - delete created office
            office_id = data["id"]
            await self.client.delete(f"{self.base_url}/offices/{office_id}")
    
    async def test_get_office(self):
        """Test 4: Get office by ID."""
        print("\n🧪 Test 4: Get Office by ID")
        
        # Assume office with ID 1 exists
        response = await self.client.get(f"{self.base_url}/offices/1")
        self.assert_status(response, 200, "Get office returns 200")
        
        if response.status_code == 200:
            data = response.json()
            self.assert_true("id" in data, "Response has 'id' field")
            self.assert_true("name" in data, "Response has 'name' field")
    
    async def test_update_office(self):
        """Test 5: Update office."""
        print("\n🧪 Test 5: Update Office")
        
        # First create an office
        office_data = {
            "name": "TEST_UPDATE_P777",
            "area": 70.0,
            "floor": 7,
            "base_price": 25000000
        }
        
        create_response = await self.client.post(f"{self.base_url}/offices", json=office_data)
        
        if create_response.status_code == 201:
            office_id = create_response.json()["id"]
            
            # Update the office
            update_data = {"base_price": 30000000}
            response = await self.client.put(f"{self.base_url}/offices/{office_id}", json=update_data)
            self.assert_status(response, 200, "Update office returns 200")
            
            if response.status_code == 200:
                data = response.json()
                self.assert_true(float(data["base_price"]) == 30000000, "Price updated correctly")
            
            # Cleanup
            await self.client.delete(f"{self.base_url}/offices/{office_id}")
        else:
            print("  ⚠️  Skipped (could not create test office)")
    
    async def test_delete_office(self):
        """Test 6: Delete office."""
        print("\n🧪 Test 6: Delete Office")
        
        # Create office to delete
        office_data = {
            "name": "TEST_DELETE_P666",
            "area": 60.0,
            "floor": 6,
            "base_price": 20000000
        }
        
        create_response = await self.client.post(f"{self.base_url}/offices", json=office_data)
        
        if create_response.status_code == 201:
            office_id = create_response.json()["id"]
            
            # Delete the office
            response = await self.client.delete(f"{self.base_url}/offices/{office_id}")
            self.assert_status(response, 200, "Delete office returns 200")
            
            # Verify it's deleted
            get_response = await self.client.get(f"{self.base_url}/offices/{office_id}")
            self.assert_status(get_response, 404, "Deleted office returns 404")
        else:
            print("  ⚠️  Skipped (could not create test office)")
    
    async def test_list_companies(self):
        """Test 7: List companies."""
        print("\n🧪 Test 7: List Companies")
        
        response = await self.client.get(f"{self.base_url}/companies")
        self.assert_status(response, 200, "List companies returns 200")
        
        if response.status_code == 200:
            data = response.json()
            self.assert_true(isinstance(data, list), "Response is a list")
    
    async def test_create_company(self):
        """Test 8: Create company."""
        print("\n🧪 Test 8: Create Company")
        
        company_data = {
            "name": "Test API Company",
            "tax_code": "API_TEST_123",
            "email": "test@apitest.com",
            "address": "123 Test Street"
        }
        
        response = await self.client.post(f"{self.base_url}/companies", json=company_data)
        self.assert_status(response, 201, "Create company returns 201")
        
        if response.status_code == 201:
            data = response.json()
            self.assert_true("id" in data, "Response has 'id' field")
            self.assert_true(data["tax_code"] == company_data["tax_code"], "Tax code matches")
            
            # Cleanup
            company_id = data["id"]
            await self.client.delete(f"{self.base_url}/companies/{company_id}")
    
    async def test_company_monthly_costs(self):
        """Test 9: Get company monthly costs."""
        print("\n🧪 Test 9: Company Monthly Costs")
        
        # Assume company with ID 1 exists
        response = await self.client.get(f"{self.base_url}/companies/1/monthly-costs?month=1&year=2026")
        self.assert_status(response, 200, "Monthly costs returns 200")
        
        if response.status_code == 200:
            data = response.json()
            # Check structure
            self.assert_true("total_cost" in data, "Response has 'total_cost'")
            self.assert_true("rent_cost" in data, "Response has 'rent_cost'")
            self.assert_true("service_costs" in data, "Response has 'service_costs'")
            self.assert_true("company_id" in data, "Response has 'company_id'")
            self.assert_true("month" in data, "Response has 'month'")
            self.assert_true("year" in data, "Response has 'year'")
            
            # Check data types
            self.assert_true(isinstance(data["total_cost"], (int, float)), "total_cost is numeric")
            self.assert_true(isinstance(data["rent_cost"], (int, float)), "rent_cost is numeric")
            self.assert_true(isinstance(data["service_costs"], list), "service_costs is list")
            
            # Check business logic
            self.assert_true(data["total_cost"] >= 0, "total_cost is non-negative")
            self.assert_true(data["month"] == 1, "month parameter correct")
            self.assert_true(data["year"] == 2026, "year parameter correct")
            
            # Check service_costs structure
            if len(data["service_costs"]) > 0:
                service = data["service_costs"][0]
                self.assert_true("service_name" in service, "service has 'service_name'")
                self.assert_true("service_cost" in service, "service has 'service_cost'")
                self.assert_true(isinstance(service["service_cost"], (int, float)), "service_cost is numeric")
    
    async def test_list_contracts(self):
        """Test 10: List rent contracts."""
        print("\n🧪 Test 10: List Rent Contracts")
        
        response = await self.client.get(f"{self.base_url}/contracts")
        self.assert_status(response, 200, "List contracts returns 200")
        
        if response.status_code == 200:
            data = response.json()
            self.assert_true(isinstance(data, list), "Response is a list")
    
    async def test_list_building_employees(self):
        """Test 11: List building employees."""
        print("\n🧪 Test 11: List Building Employees")
        
        response = await self.client.get(f"{self.base_url}/building-employees")
        self.assert_status(response, 200, "List employees returns 200")
        
        if response.status_code == 200:
            data = response.json()
            self.assert_true(isinstance(data, list), "Response is a list")
    
    async def test_employee_salaries(self):
        """Test 12: Get employee salaries."""
        print("\n🧪 Test 12: Employee Salaries")
        
        response = await self.client.get(f"{self.base_url}/building-employees/salaries/monthly?month=1&year=2026")
        self.assert_status(response, 200, "Employee salaries returns 200")
        
        if response.status_code == 200:
            data = response.json()
            self.assert_true(isinstance(data, list), "Response is a list")
            
            # Check employee salary structure
            if len(data) > 0:
                employee = data[0]
                self.assert_true("employee_id" in employee, "employee has 'employee_id'")
                self.assert_true("full_name" in employee, "employee has 'full_name'")
                self.assert_true("role" in employee, "employee has 'role'")
                self.assert_true("base_salary" in employee, "employee has 'base_salary'")
                self.assert_true("total_salary" in employee, "employee has 'total_salary'")
                self.assert_true(isinstance(employee["base_salary"], (int, float)), "base_salary is numeric")
                self.assert_true(isinstance(employee["total_salary"], (int, float)), "total_salary is numeric")
                self.assert_true(employee["total_salary"] >= employee["base_salary"], "total_salary >= base_salary")
                self.assert_true("base_salary" in employee, "employee has 'base_salary'")
                self.assert_true("total_salary" in employee, "employee has 'total_salary'")
                
                # Check data types and logic
                self.assert_true(isinstance(employee["base_salary"], (int, float)), "base_salary is numeric")
                self.assert_true(isinstance(employee["total_salary"], (int, float)), "total_salary is numeric")
                self.assert_true(employee["total_salary"] >= employee["base_salary"], 
                               "total_salary >= base_salary")
    
    async def test_pagination(self):
        """Test 13: Pagination parameters."""
        print("\n🧪 Test 13: Pagination")
        
        response = await self.client.get(f"{self.base_url}/offices?skip=0&limit=2")
        self.assert_status(response, 200, "Pagination returns 200")
        
        if response.status_code == 200:
            data = response.json()
            self.assert_true(len(data) <= 2, f"Respects limit parameter ({len(data)} <= 2)")
    
    async def test_invalid_id(self):
        """Test 14: Invalid ID returns 404."""
        print("\n🧪 Test 14: Invalid ID Handling")
        
        response = await self.client.get(f"{self.base_url}/offices/99999")
        self.assert_status(response, 404, "Invalid ID returns 404")
    
    async def test_validation_errors(self):
        """Test 15: Validation errors."""
        print("\n🧪 Test 15: Validation Errors")
        
        # Try to create office with invalid data
        invalid_data = {
            "name": "Test",
            "area": -50,  # Invalid: negative area
            "floor": 1,
            "base_price": 10000000
        }
        
        response = await self.client.post(f"{self.base_url}/offices", json=invalid_data)
        self.assert_true(response.status_code == 422, "Invalid data returns 422")
    
    async def test_company_service_details(self):
        """Test 16: Get company service details."""
        print("\n🧪 Test 16: Company Service Details")
        
        response = await self.client.get(f"{self.base_url}/companies/1/service-details?month=1&year=2026")
        self.assert_status(response, 200, "Service details returns 200")
        
        if response.status_code == 200:
            data = response.json()
            # Check structure
            self.assert_true("company_id" in data, "Response has 'company_id'")
            self.assert_true("company_name" in data, "Response has 'company_name'")
            self.assert_true("month" in data, "Response has 'month'")
            self.assert_true("year" in data, "Response has 'year'")
            self.assert_true("monthly_services" in data, "Response has 'monthly_services'")
            self.assert_true("daily_services" in data, "Response has 'daily_services'")
            self.assert_true("total_service_cost" in data, "Response has 'total_service_cost'")
            
            # Check data types
            self.assert_true(isinstance(data["monthly_services"], list), "monthly_services is list")
            self.assert_true(isinstance(data["daily_services"], list), "daily_services is list")
            self.assert_true(isinstance(data["total_service_cost"], (int, float)), "total_service_cost is numeric")
            
            # Check business logic
            self.assert_true(data["total_service_cost"] >= 0, "total_service_cost is non-negative")
            
            # Check monthly service structure if exists
            if len(data["monthly_services"]) > 0:
                service = data["monthly_services"][0]
                self.assert_true("service_name" in service, "monthly service has 'service_name'")
                self.assert_true("quantity" in service, "monthly service has 'quantity'")
                self.assert_true("unit_price" in service, "monthly service has 'unit_price'")
                self.assert_true("total_cost" in service, "monthly service has 'total_cost'")
    
    async def test_building_finance(self):
        """Test 17: Get building finance reports."""
        print("\n🧪 Test 17: Building Finance Reports")
        
        response = await self.client.get(f"{self.base_url}/reports/building-finance?month=1&year=2026")
        self.assert_status(response, 200, "Building finance returns 200")
        
        if response.status_code == 200:
            data = response.json()
            # Check structure
            self.assert_true("month" in data, "Response has 'month'")
            self.assert_true("year" in data, "Response has 'year'")
            self.assert_true("total_revenue" in data, "Response has 'total_revenue'")
            self.assert_true("total_expense" in data, "Response has 'total_expense'")
            self.assert_true("net_profit" in data, "Response has 'net_profit'")
            self.assert_true("revenue_breakdown" in data, "Response has 'revenue_breakdown'")
            
            # Check data types
            self.assert_true(isinstance(data["total_revenue"], (int, float)), "total_revenue is numeric")
            self.assert_true(isinstance(data["total_expense"], (int, float)), "total_expense is numeric")
            self.assert_true(isinstance(data["net_profit"], (int, float)), "net_profit is numeric")
            self.assert_true(isinstance(data["revenue_breakdown"], dict), "revenue_breakdown is dict")
            
            # Check business logic
            self.assert_true(data["total_revenue"] >= 0, "total_revenue is non-negative")
            self.assert_true(data["total_expense"] >= 0, "total_expense is non-negative")
            expected_profit = data["total_revenue"] - data["total_expense"]
            self.assert_true(abs(data["net_profit"] - expected_profit) < 0.01, 
                           f"net_profit calculation correct ({data['net_profit']} ≈ {expected_profit})")
            
            # Check revenue breakdown
            breakdown = data["revenue_breakdown"]
            self.assert_true("rent" in breakdown, "revenue_breakdown has 'rent'")
            self.assert_true("services" in breakdown, "revenue_breakdown has 'services'")
    
    async def test_building_finance_details(self):
        """Test 18: Get detailed building finance."""
        print("\n🧪 Test 18: Building Finance Details")
        
        response = await self.client.get(f"{self.base_url}/reports/building-finance/details?month=1&year=2026")
        self.assert_status(response, 200, "Building finance details returns 200")
        
        if response.status_code == 200:
            data = response.json()
            # Check structure
            self.assert_true("revenue_details" in data, "Response has 'revenue_details'")
            self.assert_true("expense_details" in data, "Response has 'expense_details'")
            self.assert_true("total_revenue" in data, "Response has 'total_revenue'")
            self.assert_true("total_expense" in data, "Response has 'total_expense'")
            
            # Check data types
            self.assert_true(isinstance(data["revenue_details"], list), "revenue_details is list")
            self.assert_true(isinstance(data["expense_details"], list), "expense_details is list")
            
            # Check revenue detail structure if exists
            if len(data["revenue_details"]) > 0:
                rev = data["revenue_details"][0]
                self.assert_true("company_name" in rev, "revenue detail has 'company_name'")
                self.assert_true("total_amount" in rev, "revenue detail has 'total_amount'")
            
            # Check expense detail structure if exists
            if len(data["expense_details"]) > 0:
                exp = data["expense_details"][0]
                self.assert_true("employee_name" in exp, "expense detail has 'employee_name'")
                self.assert_true("total_salary" in exp, "expense detail has 'total_salary'")
    
    async def run_all_tests(self):
        """Run all API tests."""
        print("=" * 60)
        print("🧪 RUNNING API AUTO TESTS")
        print("=" * 60)
        print(f"📌 Base URL: {self.base_url}")
        
        await self.setup()
        
        try:
            for test_name in ALL_TESTS:
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
            test_names: List of test method names (e.g. ["test_health_check", "test_list_offices"])
        """
        print("=" * 60)
        print(f"🧪 RUNNING {len(test_names)} SELECTED TEST(S)")
        print("=" * 60)
        print(f"📌 Base URL: {self.base_url}")
        print(f"📋 Tests: {', '.join(test_names)}")
        
        await self.setup()
        
        try:
            for test_name in test_names:
                if hasattr(self, test_name):
                    test_method = getattr(self, test_name)
                    await test_method()
                else:
                    print(f"\n⚠️  Unknown test: {test_name}")
                    print(f"   Available: {', '.join(ALL_TESTS)}")
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
    """
    Main test runner.
    
    Args:
        test_names: Optional list of specific test names to run.
                    If None, runs all tests.
    """
    # Check if API is running
    try:
        port = os.getenv("APP_PORT", "8222")
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://localhost:{port}/health", timeout=5.0)
            if response.status_code != 200:
                print(f"❌ API is not running at http://localhost:{port}")
                return False
    except Exception as e:
        print(f"❌ Cannot connect to API at http://localhost:{port}")
        print(f"   Error: {e}")
        return False
    
    # Run tests
    tests = APITests()
    
    if test_names:
        success = await tests.run_tests(test_names)
    else:
        success = await tests.run_all_tests()
    
    return success


if __name__ == "__main__":
    # Parse CLI arguments for individual test selection
    args = sys.argv[1:]
    
    if args and args[0] in ("--help", "-h"):
        print("Usage: python -m auto_test.api.test_api [test_name ...]")
        print("\nAvailable tests:")
        for name in ALL_TESTS:
            print(f"  {name}")
        print("\nExamples:")
        print("  python -m auto_test.api.test_api                         # Run all")
        print("  python -m auto_test.api.test_api test_health_check       # Run one")
        print("  python -m auto_test.api.test_api test_list_offices test_list_companies")
        sys.exit(0)
    
    selected = args if args else None
    success = asyncio.run(main(selected))
    sys.exit(0 if success else 1)
