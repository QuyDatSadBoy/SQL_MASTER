"""Routes package initialization."""
from api.routes import office_routes, company_routes, rent_contract_routes, building_employee_routes, report_routes

__all__ = [
    "office_routes",
    "company_routes",
    "rent_contract_routes",
    "building_employee_routes",
    "report_routes",
]
