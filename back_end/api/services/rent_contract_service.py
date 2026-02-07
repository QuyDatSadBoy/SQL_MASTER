"""
Service layer for RentContract entity.
Contains business logic.
"""
from typing import List
from fastapi import HTTPException
from api.models.rent_contract import RentContract, RentContractCreate, RentContractUpdate, RentContractWithOffice
from api.repositories.rent_contract_repository import RentContractRepository
from api.repositories.office_repository import OfficeRepository
from api.repositories.company_repository import CompanyRepository


class RentContractService:
    """Service for RentContract business logic."""
    
    def __init__(self):
        self.repository = RentContractRepository()
        self.office_repository = OfficeRepository()
        self.company_repository = CompanyRepository()
    
    async def create_contract(self, contract: RentContractCreate) -> RentContract:
        """Create a new rent contract."""
        # Validate office exists
        office = await self.office_repository.get_by_id(contract.office_id)
        if not office:
            raise HTTPException(status_code=404, detail="Văn phòng không tồn tại")
        
        # Validate company exists
        company = await self.company_repository.get_by_id(contract.company_id)
        if not company:
            raise HTTPException(status_code=404, detail="Công ty không tồn tại")
        
        # Check office availability (no overlap with existing active contracts)
        is_available = await self.office_repository.check_availability(
            contract.office_id,
            str(contract.from_date),
            str(contract.end_date)
        )
        
        if not is_available:
            raise HTTPException(
                status_code=400,
                detail="Văn phòng đã được thuê trong khoảng thời gian này"
            )
        
        contract_data = contract.model_dump()
        created = await self.repository.create(contract_data)
        return RentContract(**created)
    
    async def get_contract(self, contract_id: int) -> RentContract:
        """Get contract by ID."""
        contract = await self.repository.get_by_id(contract_id)
        if not contract:
            raise HTTPException(status_code=404, detail="Hợp đồng không tồn tại")
        return RentContract(**contract)
    
    async def list_contracts(self, skip: int = 0, limit: int = 100) -> List[RentContract]:
        """List all contracts."""
        contracts = await self.repository.get_all(skip, limit)
        return [RentContract(**contract) for contract in contracts]
    
    async def get_contracts_by_company(self, company_id: int) -> List[RentContract]:
        """Get all contracts for a company."""
        contracts = await self.repository.get_by_company(company_id)
        return [RentContract(**contract) for contract in contracts]

    async def get_contracts_by_company_with_office(self, company_id: int) -> List[RentContractWithOffice]:
        """Get all contracts for a company, kèm tên và diện tích văn phòng."""
        company = await self.company_repository.get_by_id(company_id)
        if not company:
            raise HTTPException(status_code=404, detail="Công ty không tồn tại")
        contracts = await self.repository.get_by_company_with_office(company_id)
        return [RentContractWithOffice(**c) for c in contracts]
    
    async def update_contract(self, contract_id: int, contract: RentContractUpdate) -> RentContract:
        """Update a contract."""
        # Check if contract exists
        existing = await self.repository.get_by_id(contract_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Hợp đồng không tồn tại")
        
        # If dates are being updated, check availability
        if contract.from_date or contract.end_date or contract.office_id:
            from_date = contract.from_date or existing["from_date"]
            end_date = contract.end_date or existing["end_date"]
            office_id = contract.office_id or existing["office_id"]
            
            is_available = await self.office_repository.check_availability(
                office_id,
                str(from_date),
                str(end_date),
                exclude_contract_id=contract_id
            )
            
            if not is_available:
                raise HTTPException(
                    status_code=400,
                    detail="Văn phòng đã được thuê trong khoảng thời gian này"
                )
        
        contract_data = contract.model_dump(exclude_unset=True)
        updated = await self.repository.update(contract_id, contract_data)
        
        if not updated:
            raise HTTPException(status_code=500, detail="Lỗi khi cập nhật hợp đồng")
        
        return RentContract(**updated)
    
    async def delete_contract(self, contract_id: int) -> dict:
        """Delete a contract."""
        deleted = await self.repository.delete(contract_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Hợp đồng không tồn tại")
        return {"message": "Xóa hợp đồng thành công"}
