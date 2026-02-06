"""
Routes for Company endpoints.
"""
from typing import List
from fastapi import APIRouter, Query
from api.models.company import Company, CompanyCreate, CompanyUpdate
from api.services.company_service import CompanyService

router = APIRouter(prefix="/companies", tags=["Companies"])
service = CompanyService()


@router.post("", response_model=Company, status_code=201)
async def create_company(company: CompanyCreate):
    """Tạo công ty mới."""
    return await service.create_company(company)


@router.get("/{company_id}", response_model=Company)
async def get_company(company_id: int):
    """Lấy thông tin công ty theo ID."""
    return await service.get_company(company_id)


@router.get("", response_model=List[Company])
async def list_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Liệt kê tất cả công ty."""
    return await service.list_companies(skip, limit)


@router.put("/{company_id}", response_model=Company)
async def update_company(company_id: int, company: CompanyUpdate):
    """Cập nhật thông tin công ty."""
    return await service.update_company(company_id, company)


@router.delete("/{company_id}")
async def delete_company(company_id: int):
    """Xóa công ty."""
    return await service.delete_company(company_id)


@router.get("/{company_id}/monthly-costs")
async def get_monthly_costs(
    company_id: int,
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2000, le=2100)
):
    """
    Liệt kê chi phí tháng của công ty.
    Bao gồm tiền thuê và tất cả các dịch vụ.
    """
    return await service.get_monthly_costs(company_id, month, year)


@router.get("/{company_id}/service-details")
async def get_service_details(
    company_id: int,
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2000, le=2100)
):
    """
    Chi tiết các chi phí dịch vụ của công ty.
    Bao gồm giá tiền của từng lần sử dụng dịch vụ.
    """
    return await service.get_service_details(company_id, month, year)
