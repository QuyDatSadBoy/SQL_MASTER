"""
Routes for Office endpoints.
"""
from typing import List
from fastapi import APIRouter, Query
from api.models.office import Office, OfficeCreate, OfficeUpdate
from api.services.office_service import OfficeService

router = APIRouter(prefix="/offices", tags=["Offices"])
service = OfficeService()


@router.post("", response_model=Office, status_code=201)
async def create_office(office: OfficeCreate):
    """Tạo văn phòng mới."""
    return await service.create_office(office)


@router.get("/{office_id}", response_model=Office)
async def get_office(office_id: int):
    """Lấy thông tin văn phòng theo ID."""
    return await service.get_office(office_id)


@router.get("", response_model=List[Office])
async def list_offices(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Liệt kê tất cả văn phòng."""
    return await service.list_offices(skip, limit)


@router.put("/{office_id}", response_model=Office)
async def update_office(office_id: int, office: OfficeUpdate):
    """Cập nhật thông tin văn phòng."""
    return await service.update_office(office_id, office)


@router.delete("/{office_id}")
async def delete_office(office_id: int):
    """Xóa văn phòng."""
    return await service.delete_office(office_id)
