"""
Pydantic schemas for Company entity.
"""
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional


class CompanyBase(BaseModel):
    """Base schema for Company."""
    name: str = Field(..., max_length=255, description="Tên công ty")
    tax_code: str = Field(..., max_length=50, description="Mã số thuế (unique)")
    email: Optional[EmailStr] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=255, description="Địa chỉ trụ sở chính")


class CompanyCreate(CompanyBase):
    """Schema for creating a Company."""
    pass


class CompanyUpdate(BaseModel):
    """Schema for updating a Company."""
    name: Optional[str] = Field(None, max_length=255)
    tax_code: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=255)


class Company(CompanyBase):
    """Schema for Company response."""
    id: int
    
    model_config = ConfigDict(from_attributes=True)
