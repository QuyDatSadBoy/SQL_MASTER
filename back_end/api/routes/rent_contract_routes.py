"""
Routes for RentContract endpoints.
"""
from typing import List
from fastapi import APIRouter, Query
from api.models.rent_contract import RentContract, RentContractCreate, RentContractUpdate, RentContractWithOffice
from api.services.rent_contract_service import RentContractService

router = APIRouter(prefix="/contracts", tags=["Rent Contracts"])
service = RentContractService()


@router.post("", response_model=RentContract, status_code=201)
async def create_contract(contract: RentContractCreate):
    """Tạo hợp đồng thuê mới."""
    return await service.create_contract(contract)


@router.get("/{contract_id}", response_model=RentContract)
async def get_contract(contract_id: int):
    """Lấy thông tin hợp đồng theo ID."""
    return await service.get_contract(contract_id)


@router.get("", response_model=List[RentContract])
async def list_contracts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Liệt kê tất cả hợp đồng."""
    return await service.list_contracts(skip, limit)


@router.get("/company/{company_id}", response_model=List[RentContractWithOffice])
async def get_contracts_by_company(company_id: int):
    """Lấy tất cả hợp đồng của một công ty (kèm tên và diện tích văn phòng)."""
    return await service.get_contracts_by_company_with_office(company_id)


@router.put("/{contract_id}", response_model=RentContract)
async def update_contract(contract_id: int, contract: RentContractUpdate):
    """Cập nhật hợp đồng."""
    return await service.update_contract(contract_id, contract)


@router.delete("/{contract_id}")
async def delete_contract(contract_id: int):
    """Xóa hợp đồng."""
    return await service.delete_contract(contract_id)
