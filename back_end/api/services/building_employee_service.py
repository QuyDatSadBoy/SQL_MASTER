"""
Service layer for BuildingEmployee entity.
Contains business logic.
"""
from typing import List
from fastapi import HTTPException
from api.models.building_employee import BuildingEmployee, BuildingEmployeeCreate, BuildingEmployeeUpdate
from api.repositories.building_employee_repository import BuildingEmployeeRepository


class BuildingEmployeeService:
    """Service for BuildingEmployee business logic."""
    
    def __init__(self):
        self.repository = BuildingEmployeeRepository()
    
    async def create_employee(self, employee: BuildingEmployeeCreate) -> BuildingEmployee:
        """Create a new building employee."""
        employee_data = employee.model_dump()
        created = await self.repository.create(employee_data)
        return BuildingEmployee(**created)
    
    async def get_employee(self, employee_id: int) -> BuildingEmployee:
        """Get employee by ID."""
        employee = await self.repository.get_by_id(employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail="Nhân viên không tồn tại")
        return BuildingEmployee(**employee)
    
    async def list_employees(self, skip: int = 0, limit: int = 100) -> List[BuildingEmployee]:
        """List all employees."""
        employees = await self.repository.get_all(skip, limit)
        return [BuildingEmployee(**employee) for employee in employees]
    
    async def update_employee(self, employee_id: int, employee: BuildingEmployeeUpdate) -> BuildingEmployee:
        """Update an employee."""
        # Check if employee exists
        existing = await self.repository.get_by_id(employee_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Nhân viên không tồn tại")
        
        employee_data = employee.model_dump(exclude_unset=True)
        updated = await self.repository.update(employee_id, employee_data)
        
        if not updated:
            raise HTTPException(status_code=500, detail="Lỗi khi cập nhật nhân viên")
        
        return BuildingEmployee(**updated)
    
    async def delete_employee(self, employee_id: int) -> dict:
        """Delete an employee."""
        deleted = await self.repository.delete(employee_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Nhân viên không tồn tại")
        return {"message": "Xóa nhân viên thành công"}
    
    async def get_salaries(self, month: int, year: int) -> List[dict]:
        """Get employee salaries for a specific month."""
        if month < 1 or month > 12:
            raise HTTPException(status_code=400, detail="Tháng không hợp lệ (1-12)")
        
        if year < 2000 or year > 2100:
            raise HTTPException(status_code=400, detail="Năm không hợp lệ")
        
        salaries = await self.repository.get_salaries(month, year)
        return salaries
