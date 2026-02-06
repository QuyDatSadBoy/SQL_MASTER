"""
Pydantic schemas for CompanyMonthlyUsage entity.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from decimal import Decimal
from datetime import date


class CompanyMonthlyUsageBase(BaseModel):
    """Base schema for CompanyMonthlyUsage."""
    company_id: int = Field(..., description="ID công ty")
    service_id: int = Field(..., description="ID dịch vụ")
    invoice_id: Optional[int] = Field(None, description="ID hóa đơn")
    from_date: Optional[date] = Field(None, description="Từ ngày")
    to_date: Optional[date] = Field(None, description="Đến ngày")
    quantity: Optional[int] = Field(None, description="Số lượng nhân viên hoặc m2 làm căn cứ tính")
    price: Optional[Decimal] = Field(None, description="Thành tiền tháng đó")


class CompanyMonthlyUsageCreate(CompanyMonthlyUsageBase):
    """Schema for creating a CompanyMonthlyUsage."""
    pass


class CompanyMonthlyUsageUpdate(BaseModel):
    """Schema for updating a CompanyMonthlyUsage."""
    company_id: Optional[int] = None
    service_id: Optional[int] = None
    invoice_id: Optional[int] = None
    from_date: Optional[date] = None
    to_date: Optional[date] = None
    quantity: Optional[int] = None
    price: Optional[Decimal] = None


class CompanyMonthlyUsage(CompanyMonthlyUsageBase):
    """Schema for CompanyMonthlyUsage response."""
    id: int
    
    model_config = ConfigDict(from_attributes=True)
