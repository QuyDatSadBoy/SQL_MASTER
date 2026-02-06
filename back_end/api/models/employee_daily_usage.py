"""
Pydantic schemas for EmployeeDailyUsage entity.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from decimal import Decimal
from datetime import date


class EmployeeDailyUsageBase(BaseModel):
    """Base schema for EmployeeDailyUsage."""
    employee_id: int = Field(..., description="ID nhân viên công ty khách thuê")
    invoice_id: Optional[int] = Field(None, description="ID hóa đơn")
    service_id: int = Field(..., description="ID dịch vụ")
    usage_date: date = Field(..., description="Ngày sử dụng")
    price: Optional[Decimal] = Field(None, description="Giá")
    service_type: Optional[str] = Field(None, max_length=50, description="parking, meal...")


class EmployeeDailyUsageCreate(EmployeeDailyUsageBase):
    """Schema for creating an EmployeeDailyUsage."""
    pass


class EmployeeDailyUsageUpdate(BaseModel):
    """Schema for updating an EmployeeDailyUsage."""
    employee_id: Optional[int] = None
    invoice_id: Optional[int] = None
    service_id: Optional[int] = None
    usage_date: Optional[date] = None
    price: Optional[Decimal] = None
    service_type: Optional[str] = Field(None, max_length=50)


class EmployeeDailyUsage(EmployeeDailyUsageBase):
    """Schema for EmployeeDailyUsage response."""
    id: int
    
    model_config = ConfigDict(from_attributes=True)
