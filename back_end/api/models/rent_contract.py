"""
Pydantic schemas for RentContract entity.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from decimal import Decimal
from datetime import date


class RentContractBase(BaseModel):
    """Base schema for RentContract."""
    office_id: int = Field(..., description="ID văn phòng")
    company_id: int = Field(..., description="ID công ty thuê")
    invoice_id: Optional[int] = Field(None, description="Hóa đơn thanh toán tiền cọc/lần đầu")
    from_date: date = Field(..., description="Ngày bắt đầu thuê")
    end_date: date = Field(..., description="Ngày kết thúc thuê")
    signed_date: Optional[date] = Field(None, description="Ngày ký hợp đồng")
    rent_price: Decimal = Field(..., gt=0, description="Giá chốt trong hợp đồng")
    status: Optional[str] = Field("active", max_length=20, description="active, expired, terminated")


class RentContractCreate(RentContractBase):
    """Schema for creating a RentContract."""
    pass


class RentContractUpdate(BaseModel):
    """Schema for updating a RentContract."""
    office_id: Optional[int] = None
    company_id: Optional[int] = None
    invoice_id: Optional[int] = None
    from_date: Optional[date] = None
    end_date: Optional[date] = None
    signed_date: Optional[date] = None
    rent_price: Optional[Decimal] = Field(None, gt=0)
    status: Optional[str] = Field(None, max_length=20)


class RentContract(RentContractBase):
    """Schema for RentContract response."""
    id: int
    
    model_config = ConfigDict(from_attributes=True)
