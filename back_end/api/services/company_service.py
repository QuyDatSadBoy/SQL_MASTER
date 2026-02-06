"""
Service layer for Company entity.
Contains business logic.
"""
from typing import List, Optional
from fastapi import HTTPException
from api.models.company import Company, CompanyCreate, CompanyUpdate
from api.repositories.company_repository import CompanyRepository


class CompanyService:
    """Service for Company business logic."""
    
    def __init__(self):
        self.repository = CompanyRepository()
    
    async def create_company(self, company: CompanyCreate) -> Company:
        """Create a new company."""
        # Check if tax_code already exists
        existing = await self.repository.get_by_tax_code(company.tax_code)
        if existing:
            raise HTTPException(
                status_code=400, 
                detail=f"Mã số thuế {company.tax_code} đã tồn tại"
            )
        
        company_data = company.model_dump()
        created = await self.repository.create(company_data)
        return Company(**created)
    
    async def get_company(self, company_id: int) -> Company:
        """Get company by ID."""
        company = await self.repository.get_by_id(company_id)
        if not company:
            raise HTTPException(status_code=404, detail="Công ty không tồn tại")
        return Company(**company)
    
    async def list_companies(self, skip: int = 0, limit: int = 100) -> List[Company]:
        """List all companies."""
        companies = await self.repository.get_all(skip, limit)
        return [Company(**company) for company in companies]
    
    async def update_company(self, company_id: int, company: CompanyUpdate) -> Company:
        """Update a company."""
        # Check if company exists
        existing = await self.repository.get_by_id(company_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Công ty không tồn tại")
        
        # Check if new tax_code conflicts
        if company.tax_code:
            existing_tax = await self.repository.get_by_tax_code(company.tax_code)
            if existing_tax and existing_tax["id"] != company_id:
                raise HTTPException(
                    status_code=400,
                    detail=f"Mã số thuế {company.tax_code} đã tồn tại"
                )
        
        company_data = company.model_dump(exclude_unset=True)
        updated = await self.repository.update(company_id, company_data)
        
        if not updated:
            raise HTTPException(status_code=500, detail="Lỗi khi cập nhật công ty")
        
        return Company(**updated)
    
    async def delete_company(self, company_id: int) -> dict:
        """Delete a company."""
        deleted = await self.repository.delete(company_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Công ty không tồn tại")
        return {"message": "Xóa công ty thành công"}
    
    async def get_monthly_costs(self, company_id: int, month: int, year: int) -> dict:
        """Get company's monthly costs."""
        # Check if company exists
        company = await self.repository.get_by_id(company_id)
        if not company:
            raise HTTPException(status_code=404, detail="Công ty không tồn tại")
        
        costs = await self.repository.get_monthly_costs(company_id, month, year)
        return costs
    
    async def get_service_details(self, company_id: int, month: int, year: int) -> dict:
        """Get detailed service usage and costs for a company."""
        # Check if company exists
        company = await self.repository.get_by_id(company_id)
        if not company:
            raise HTTPException(status_code=404, detail="Công ty không tồn tại")
        
        details = await self.repository.get_service_details(company_id, month, year)
        return details
