"""
API Utilities & Toolkit for Auto Testing + Agent Debugging
100% raw HTTP calls via httpx

Cách dùng:
    # 1. Import và gọi từng API
    from auto_test.api.api_utils import APIExplorer
    explorer = APIExplorer()
    await explorer.list_offices()
    await explorer.get_company_monthly_costs(1, month=1, year=2026)
    await explorer.get_building_finance(month=1, year=2026, save_to="finance.json")
    await explorer.close()

    # 2. Gọi generic
    await explorer.call_api("GET", "/offices/1")
    await explorer.call_api("POST", "/offices", json_body={"name": "P101", ...})

    # 3. Dùng standalone functions
    from auto_test.api.api_utils import call_api, list_offices, get_office
    result = await list_offices()
    result = await get_office(1, save_to="office_1.json")
"""
import os
import sys
import json
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional, List, Union
from dotenv import load_dotenv

import httpx

load_dotenv()

# Output directory for JSON files
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")


def _get_base_url() -> str:
    port = os.getenv("APP_PORT", "8222")
    return f"http://localhost:{port}/api"


def _ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def _save_json(data: Any, filepath: str):
    """Save data to JSON file."""
    _ensure_output_dir()
    if not os.path.isabs(filepath):
        filepath = os.path.join(OUTPUT_DIR, filepath)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    print(f"  💾 Saved to: {filepath}")


def _print_request(method: str, url: str, body: Any = None, params: Dict = None):
    """Print request info."""
    print(f"\n{'='*60}")
    print(f"📤 REQUEST: {method} {url}")
    if params:
        print(f"   Params: {json.dumps(params, default=str)}")
    if body:
        print(f"   Body: {json.dumps(body, ensure_ascii=False, default=str)}")
    print(f"{'='*60}")


def _print_response(status: int, data: Any, truncate: int = 2000):
    """Print response info with optional truncation."""
    status_icon = "✅" if 200 <= status < 300 else "❌"
    print(f"{status_icon} RESPONSE: {status}")

    text = json.dumps(data, ensure_ascii=False, indent=2, default=str)
    if len(text) > truncate:
        print(f"   (Showing first {truncate} chars, total {len(text)} chars)")
        print(f"   {text[:truncate]}...")
        print(f"   ... (truncated, use save_to='file.json' to see full output)")
    else:
        print(f"   {text}")


# =============================================================
# APIClient - Low-level HTTP client (kept for test_api.py)
# =============================================================

class APIClient:
    """Low-level async HTTP client for API calls."""

    def __init__(self, base_url: Optional[str] = None):
        if base_url is None:
            port = os.getenv("APP_PORT", "8222")
            base_url = f"http://localhost:{port}/api"
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)

    async def close(self):
        await self.client.aclose()

    async def get(self, endpoint: str, **kwargs) -> httpx.Response:
        return await self.client.get(f"{self.base_url}{endpoint}", **kwargs)

    async def post(self, endpoint: str, **kwargs) -> httpx.Response:
        return await self.client.post(f"{self.base_url}{endpoint}", **kwargs)

    async def put(self, endpoint: str, **kwargs) -> httpx.Response:
        return await self.client.put(f"{self.base_url}{endpoint}", **kwargs)

    async def delete(self, endpoint: str, **kwargs) -> httpx.Response:
        return await self.client.delete(f"{self.base_url}{endpoint}", **kwargs)


# =============================================================
# APIExplorer - High-level API toolkit for agent
# Agent có thể import class này để gọi từng API,
# xem input/output, lưu vào JSON khi cần.
# =============================================================

class APIExplorer:
    """
    High-level API explorer for debugging & inspection.

    Features:
    - Gọi từng API endpoint riêng biệt
    - In input/output rõ ràng
    - Lưu output vào JSON file khi cần (save_to parameter)
    - Generic call_api() cho bất kỳ endpoint nào

    Usage:
        explorer = APIExplorer()
        data = await explorer.list_offices()
        data = await explorer.get_company_monthly_costs(1, month=1, year=2026, save_to="costs.json")
        await explorer.close()
    """

    def __init__(self, base_url: Optional[str] = None, verbose: bool = True):
        self.base_url = base_url or _get_base_url()
        self.client = httpx.AsyncClient(timeout=30.0)
        self.verbose = verbose

    async def close(self):
        await self.client.aclose()

    async def call_api(
        self,
        method: str,
        endpoint: str,
        json_body: Any = None,
        params: Dict = None,
        save_to: Optional[str] = None,
        verbose: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Generic API call. Returns dict with status, data, success.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (e.g. "/offices", "/companies/1/monthly-costs")
            json_body: Request body for POST/PUT
            params: Query parameters
            save_to: File path to save JSON output (relative to output/ dir)
            verbose: Override verbose setting

        Returns:
            {"status": int, "data": Any, "success": bool, "url": str}
        """
        url = f"{self.base_url}{endpoint}"
        show = verbose if verbose is not None else self.verbose

        if show:
            _print_request(method, url, json_body, params)

        try:
            response = await self.client.request(
                method=method.upper(),
                url=url,
                json=json_body,
                params=params
            )

            try:
                data = response.json()
            except Exception:
                data = response.text

            result = {
                "status": response.status_code,
                "data": data,
                "success": 200 <= response.status_code < 300,
                "url": url
            }

            if show:
                _print_response(response.status_code, data)

            if save_to:
                _save_json(result, save_to)

            return result

        except httpx.ConnectError:
            print(f"❌ Cannot connect to {url} - Is the API server running?")
            return {"status": 0, "data": None, "success": False, "url": url}
        except Exception as e:
            print(f"❌ Error: {e}")
            return {"status": 0, "data": str(e), "success": False, "url": url}

    # ---------------------------------------------------------
    # Health Check
    # ---------------------------------------------------------

    async def health_check(self, save_to: Optional[str] = None) -> Dict:
        """Check API health status."""
        return await self.call_api("GET", "/../health", save_to=save_to)

    # ---------------------------------------------------------
    # Offices
    # ---------------------------------------------------------

    async def list_offices(
        self, skip: int = 0, limit: int = 100, save_to: Optional[str] = None
    ) -> Dict:
        """List all offices with pagination."""
        return await self.call_api(
            "GET", "/offices", params={"skip": skip, "limit": limit}, save_to=save_to
        )

    async def get_office(self, office_id: int, save_to: Optional[str] = None) -> Dict:
        """Get a single office by ID."""
        return await self.call_api("GET", f"/offices/{office_id}", save_to=save_to)

    async def create_office(self, data: Dict[str, Any], save_to: Optional[str] = None) -> Dict:
        """
        Create a new office.

        Args:
            data: {"name": str, "area": float, "floor": int, "base_price": float, "position": str?}
        """
        return await self.call_api("POST", "/offices", json_body=data, save_to=save_to)

    async def update_office(
        self, office_id: int, data: Dict[str, Any], save_to: Optional[str] = None
    ) -> Dict:
        """Update an office."""
        return await self.call_api("PUT", f"/offices/{office_id}", json_body=data, save_to=save_to)

    async def delete_office(self, office_id: int, save_to: Optional[str] = None) -> Dict:
        """Delete an office."""
        return await self.call_api("DELETE", f"/offices/{office_id}", save_to=save_to)

    # ---------------------------------------------------------
    # Companies
    # ---------------------------------------------------------

    async def list_companies(
        self, skip: int = 0, limit: int = 100, save_to: Optional[str] = None
    ) -> Dict:
        """List all companies with pagination."""
        return await self.call_api(
            "GET", "/companies", params={"skip": skip, "limit": limit}, save_to=save_to
        )

    async def get_company(self, company_id: int, save_to: Optional[str] = None) -> Dict:
        """Get a single company by ID."""
        return await self.call_api("GET", f"/companies/{company_id}", save_to=save_to)

    async def create_company(self, data: Dict[str, Any], save_to: Optional[str] = None) -> Dict:
        """
        Create a new company.

        Args:
            data: {"name": str, "tax_code": str, "email": str, "address": str?}
        """
        return await self.call_api("POST", "/companies", json_body=data, save_to=save_to)

    async def update_company(
        self, company_id: int, data: Dict[str, Any], save_to: Optional[str] = None
    ) -> Dict:
        """Update a company."""
        return await self.call_api("PUT", f"/companies/{company_id}", json_body=data, save_to=save_to)

    async def delete_company(self, company_id: int, save_to: Optional[str] = None) -> Dict:
        """Delete a company."""
        return await self.call_api("DELETE", f"/companies/{company_id}", save_to=save_to)

    # ---------------------------------------------------------
    # Company Reports (Monthly costs, Service details)
    # ---------------------------------------------------------

    async def get_company_monthly_costs(
        self,
        company_id: int,
        month: int = 1,
        year: int = 2026,
        save_to: Optional[str] = None
    ) -> Dict:
        """
        Get monthly costs for a company.

        Returns: {company_id, month, year, rent_cost, service_costs[], total_cost}
        """
        return await self.call_api(
            "GET",
            f"/companies/{company_id}/monthly-costs",
            params={"month": month, "year": year},
            save_to=save_to
        )

    async def get_company_service_details(
        self,
        company_id: int,
        month: int = 1,
        year: int = 2026,
        save_to: Optional[str] = None
    ) -> Dict:
        """
        Get detailed service breakdown for a company.

        Returns: {company_id, company_name, month, year,
                  monthly_services[], daily_services[], total_service_cost}
        """
        return await self.call_api(
            "GET",
            f"/companies/{company_id}/service-details",
            params={"month": month, "year": year},
            save_to=save_to
        )

    # ---------------------------------------------------------
    # Contracts
    # ---------------------------------------------------------

    async def list_contracts(self, save_to: Optional[str] = None) -> Dict:
        """List all rent contracts."""
        return await self.call_api("GET", "/contracts", save_to=save_to)

    # ---------------------------------------------------------
    # Building Employees
    # ---------------------------------------------------------

    async def list_building_employees(self, save_to: Optional[str] = None) -> Dict:
        """List all building employees."""
        return await self.call_api("GET", "/building-employees", save_to=save_to)

    async def get_employee_salaries(
        self,
        month: int = 1,
        year: int = 2026,
        save_to: Optional[str] = None
    ) -> Dict:
        """
        Get monthly salaries for all building employees.

        Returns: [{employee_id, full_name, role, base_salary, total_salary, ...}]
        """
        return await self.call_api(
            "GET",
            "/building-employees/salaries/monthly",
            params={"month": month, "year": year},
            save_to=save_to
        )

    # ---------------------------------------------------------
    # Building Finance Reports
    # ---------------------------------------------------------

    async def get_building_finance(
        self,
        month: int = 1,
        year: int = 2026,
        save_to: Optional[str] = None
    ) -> Dict:
        """
        Get building finance summary.

        Returns: {month, year, total_revenue, total_expense, net_profit, revenue_breakdown}
        """
        return await self.call_api(
            "GET",
            "/reports/building-finance",
            params={"month": month, "year": year},
            save_to=save_to
        )

    async def get_building_finance_details(
        self,
        month: int = 1,
        year: int = 2026,
        save_to: Optional[str] = None
    ) -> Dict:
        """
        Get detailed building finance (revenue + expense breakdown).

        Returns: {total_revenue, total_expense, revenue_details[], expense_details[]}
        """
        return await self.call_api(
            "GET",
            "/reports/building-finance/details",
            params={"month": month, "year": year},
            save_to=save_to
        )

    # ---------------------------------------------------------
    # Batch: Call all report APIs and save to JSON
    # ---------------------------------------------------------

    async def dump_all_reports(
        self,
        month: int = 1,
        year: int = 2026,
        output_dir: str = "reports"
    ) -> Dict:
        """
        Call all report endpoints and save to JSON files.
        Useful for full inspection.
        """
        print(f"\n🔄 Dumping all reports for {month}/{year}...")

        results = {}

        # All companies monthly costs
        companies = await self.list_companies(verbose=False)
        if companies["success"]:
            for company in companies["data"]:
                cid = company["id"]
                costs = await self.get_company_monthly_costs(
                    cid, month, year,
                    save_to=f"{output_dir}/company_{cid}_costs.json"
                )
                results[f"company_{cid}_costs"] = costs["success"]

                details = await self.get_company_service_details(
                    cid, month, year,
                    save_to=f"{output_dir}/company_{cid}_services.json"
                )
                results[f"company_{cid}_services"] = details["success"]

        # Employee salaries
        salaries = await self.get_employee_salaries(
            month, year, save_to=f"{output_dir}/salaries.json"
        )
        results["salaries"] = salaries["success"]

        # Building finance
        finance = await self.get_building_finance(
            month, year, save_to=f"{output_dir}/finance_summary.json"
        )
        results["finance_summary"] = finance["success"]

        finance_details = await self.get_building_finance_details(
            month, year, save_to=f"{output_dir}/finance_details.json"
        )
        results["finance_details"] = finance_details["success"]

        # Summary
        passed = sum(1 for v in results.values() if v)
        total = len(results)
        print(f"\n📊 Dump complete: {passed}/{total} succeeded")
        print(f"📁 Files saved to: {os.path.join(OUTPUT_DIR, output_dir)}/")

        return results


# =============================================================
# Standalone functions - for quick one-off calls
# Usage: from auto_test.api.api_utils import list_offices
#        result = await list_offices()
# =============================================================

async def call_api(
    method: str,
    endpoint: str,
    json_body: Any = None,
    params: Dict = None,
    save_to: Optional[str] = None,
    verbose: bool = True
) -> Dict:
    """Generic standalone API call."""
    explorer = APIExplorer(verbose=verbose)
    try:
        return await explorer.call_api(method, endpoint, json_body, params, save_to)
    finally:
        await explorer.close()


async def list_offices(save_to: Optional[str] = None) -> Dict:
    """List all offices."""
    return await call_api("GET", "/offices", save_to=save_to)


async def get_office(office_id: int, save_to: Optional[str] = None) -> Dict:
    """Get office by ID."""
    return await call_api("GET", f"/offices/{office_id}", save_to=save_to)


async def create_office(data: Dict, save_to: Optional[str] = None) -> Dict:
    """Create office."""
    return await call_api("POST", "/offices", json_body=data, save_to=save_to)


async def update_office(office_id: int, data: Dict, save_to: Optional[str] = None) -> Dict:
    """Update office."""
    return await call_api("PUT", f"/offices/{office_id}", json_body=data, save_to=save_to)


async def delete_office(office_id: int, save_to: Optional[str] = None) -> Dict:
    """Delete office."""
    return await call_api("DELETE", f"/offices/{office_id}", save_to=save_to)


async def list_companies(save_to: Optional[str] = None) -> Dict:
    """List all companies."""
    return await call_api("GET", "/companies", save_to=save_to)


async def get_company(company_id: int, save_to: Optional[str] = None) -> Dict:
    """Get company by ID."""
    return await call_api("GET", f"/companies/{company_id}", save_to=save_to)


async def create_company(data: Dict, save_to: Optional[str] = None) -> Dict:
    """Create company."""
    return await call_api("POST", "/companies", json_body=data, save_to=save_to)


async def update_company(company_id: int, data: Dict, save_to: Optional[str] = None) -> Dict:
    """Update company."""
    return await call_api("PUT", f"/companies/{company_id}", json_body=data, save_to=save_to)


async def delete_company(company_id: int, save_to: Optional[str] = None) -> Dict:
    """Delete company."""
    return await call_api("DELETE", f"/companies/{company_id}", save_to=save_to)


async def get_company_monthly_costs(
    company_id: int, month: int = 1, year: int = 2026, save_to: Optional[str] = None
) -> Dict:
    """Get company monthly costs."""
    return await call_api(
        "GET", f"/companies/{company_id}/monthly-costs",
        params={"month": month, "year": year}, save_to=save_to
    )


async def get_company_service_details(
    company_id: int, month: int = 1, year: int = 2026, save_to: Optional[str] = None
) -> Dict:
    """Get company service details."""
    return await call_api(
        "GET", f"/companies/{company_id}/service-details",
        params={"month": month, "year": year}, save_to=save_to
    )


async def list_contracts(save_to: Optional[str] = None) -> Dict:
    """List all contracts."""
    return await call_api("GET", "/contracts", save_to=save_to)


async def list_building_employees(save_to: Optional[str] = None) -> Dict:
    """List all building employees."""
    return await call_api("GET", "/building-employees", save_to=save_to)


async def get_employee_salaries(
    month: int = 1, year: int = 2026, save_to: Optional[str] = None
) -> Dict:
    """Get employee salaries."""
    return await call_api(
        "GET", "/building-employees/salaries/monthly",
        params={"month": month, "year": year}, save_to=save_to
    )


async def get_building_finance(
    month: int = 1, year: int = 2026, save_to: Optional[str] = None
) -> Dict:
    """Get building finance summary."""
    return await call_api(
        "GET", "/reports/building-finance",
        params={"month": month, "year": year}, save_to=save_to
    )


async def get_building_finance_details(
    month: int = 1, year: int = 2026, save_to: Optional[str] = None
) -> Dict:
    """Get building finance details."""
    return await call_api(
        "GET", "/reports/building-finance/details",
        params={"month": month, "year": year}, save_to=save_to
    )


# =============================================================
# CLI Entry Point
# =============================================================

if __name__ == "__main__":
    async def main():
        explorer = APIExplorer()

        try:
            # Health check
            await explorer.health_check()

            # List resources
            await explorer.list_offices()
            await explorer.list_companies()
            await explorer.list_contracts()
            await explorer.list_building_employees()

            # Reports
            await explorer.get_employee_salaries(month=1, year=2026)
            await explorer.get_building_finance(month=1, year=2026)
            await explorer.get_building_finance_details(
                month=1, year=2026, save_to="finance_details.json"
            )

        finally:
            await explorer.close()

    asyncio.run(main())
