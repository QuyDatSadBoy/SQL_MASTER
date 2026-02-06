"""
Pydantic schemas for Invoice entity.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from decimal import Decimal
from datetime import date


class InvoiceBase(BaseModel):
    """Base schema for Invoice."""
    created_date: Optional[date] = None
    pay_day: Optional[date] = Field(None, description="Ngày thanh toán")
    from_date: Optional[date] = Field(None, description="Kỳ thanh toán từ ngày")
    to_date: Optional[date] = Field(None, description="Kỳ thanh toán đến ngày")
    total_amount: Optional[Decimal] = Field(None, description="Tổng tiền")
    status: Optional[str] = Field("unpaid", max_length=20, description="paid, unpaid, overdue")
    note: Optional[str] = None


class InvoiceCreate(InvoiceBase):
    """Schema for creating an Invoice."""
    pass


class InvoiceUpdate(BaseModel):
    """Schema for updating an Invoice."""
    created_date: Optional[date] = None
    pay_day: Optional[date] = None
    from_date: Optional[date] = None
    to_date: Optional[date] = None
    total_amount: Optional[Decimal] = None
    status: Optional[str] = Field(None, max_length=20)
    note: Optional[str] = None


class Invoice(InvoiceBase):
    """Schema for Invoice response."""
    id: int
    
    model_config = ConfigDict(from_attributes=True)
