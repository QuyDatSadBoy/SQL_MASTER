"""
Pydantic schemas for BuildingEmployee entity.
"""
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional
from decimal import Decimal
from datetime import date


class BuildingEmployeeBase(BaseModel):
    """Base schema for BuildingEmployee."""
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    phone_number: Optional[str] = Field(None, max_length=20)
    role: str = Field(..., max_length=50, description="Vai trò lúc làm việc này")
    email: Optional[EmailStr] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=255)
    date_of_birth: Optional[date] = None
    base_salary: Optional[Decimal] = Field(None, description="Lương cơ bản/cứng")
    hire_date: Optional[date] = None
    status: Optional[str] = Field(None, max_length=20)


class BuildingEmployeeCreate(BuildingEmployeeBase):
    """Schema for creating a BuildingEmployee."""
    pass


class BuildingEmployeeUpdate(BaseModel):
    """Schema for updating a BuildingEmployee."""
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    phone_number: Optional[str] = Field(None, max_length=20)
    role: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=255)
    date_of_birth: Optional[date] = None
    base_salary: Optional[Decimal] = None
    hire_date: Optional[date] = None
    status: Optional[str] = Field(None, max_length=20)


class BuildingEmployee(BuildingEmployeeBase):
    """Schema for BuildingEmployee response."""
    employee_id: int
    
    model_config = ConfigDict(from_attributes=True)
