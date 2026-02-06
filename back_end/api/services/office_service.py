"""
Service layer for Office entity.
Contains business logic.
"""
from typing import List, Optional
from fastapi import HTTPException
from api.models.office import Office, OfficeCreate, OfficeUpdate
from api.repositories.office_repository import OfficeRepository


class OfficeService:
    """Service for Office business logic."""
    
    def __init__(self):
        self.repository = OfficeRepository()
    
    async def create_office(self, office: OfficeCreate) -> Office:
        """Create a new office."""
        office_data = office.model_dump()
        created = await self.repository.create(office_data)
        return Office(**created)
    
    async def get_office(self, office_id: int) -> Office:
        """Get office by ID."""
        office = await self.repository.get_by_id(office_id)
        if not office:
            raise HTTPException(status_code=404, detail="Văn phòng không tồn tại")
        return Office(**office)
    
    async def list_offices(self, skip: int = 0, limit: int = 100) -> List[Office]:
        """List all offices."""
        offices = await self.repository.get_all(skip, limit)
        return [Office(**office) for office in offices]
    
    async def update_office(self, office_id: int, office: OfficeUpdate) -> Office:
        """Update an office."""
        # Check if office exists
        existing = await self.repository.get_by_id(office_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Văn phòng không tồn tại")
        
        office_data = office.model_dump(exclude_unset=True)
        updated = await self.repository.update(office_id, office_data)
        
        if not updated:
            raise HTTPException(status_code=500, detail="Lỗi khi cập nhật văn phòng")
        
        return Office(**updated)
    
    async def delete_office(self, office_id: int) -> dict:
        """Delete an office."""
        deleted = await self.repository.delete(office_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Văn phòng không tồn tại")
        return {"message": "Xóa văn phòng thành công"}
