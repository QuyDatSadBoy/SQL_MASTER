"""
Pydantic schemas for CompanyEmployee entity.
"""
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional


class CompanyEmployeeBase(BaseModel):
    """Base schema for CompanyEmployee."""
    company_id: int = Field(..., description="ID công ty")
    full_name: str = Field(..., max_length=100, description="Họ tên nhân viên")
    job_title: Optional[str] = Field(None, max_length=100, description="Chức vụ")
    phone_number: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = Field(None, max_length=100)
    status: Optional[str] = Field("working", max_length=20, description="working, resigned")


class CompanyEmployeeCreate(CompanyEmployeeBase):
    """Schema for creating a CompanyEmployee."""
    pass


class CompanyEmployeeUpdate(BaseModel):
    """Schema for updating a CompanyEmployee."""
    company_id: Optional[int] = None
    full_name: Optional[str] = Field(None, max_length=100)
    job_title: Optional[str] = Field(None, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = Field(None, max_length=100)
    status: Optional[str] = Field(None, max_length=20)


class CompanyEmployee(CompanyEmployeeBase):
    """Schema for CompanyEmployee response."""
    id: int
    
    model_config = ConfigDict(from_attributes=True)
