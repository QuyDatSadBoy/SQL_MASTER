"""
Routes for BuildingEmployee endpoints.
"""
from typing import List
from fastapi import APIRouter, Query
from api.models.building_employee import BuildingEmployee, BuildingEmployeeCreate, BuildingEmployeeUpdate
from api.services.building_employee_service import BuildingEmployeeService

router = APIRouter(prefix="/building-employees", tags=["Building Employees"])
service = BuildingEmployeeService()


@router.post("", response_model=BuildingEmployee, status_code=201)
async def create_employee(employee: BuildingEmployeeCreate):
    """Tạo nhân viên tòa nhà mới."""
    return await service.create_employee(employee)


@router.get("/{employee_id}", response_model=BuildingEmployee)
async def get_employee(employee_id: int):
    """Lấy thông tin nhân viên theo ID."""
    return await service.get_employee(employee_id)


@router.get("", response_model=List[BuildingEmployee])
async def list_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Liệt kê tất cả nhân viên tòa nhà."""
    return await service.list_employees(skip, limit)


@router.put("/{employee_id}", response_model=BuildingEmployee)
async def update_employee(employee_id: int, employee: BuildingEmployeeUpdate):
    """Cập nhật thông tin nhân viên."""
    return await service.update_employee(employee_id, employee)


@router.delete("/{employee_id}")
async def delete_employee(employee_id: int):
    """Xóa nhân viên."""
    return await service.delete_employee(employee_id)


@router.get("/salaries/monthly")
async def get_employee_salaries(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2000, le=2100)
):
    """
    Liệt kê lương của tất cả nhân viên tòa nhà trong tháng.
    Lương = base_salary + (doanh thu * bonus_rate)
    """
    return await service.get_salaries(month, year)
