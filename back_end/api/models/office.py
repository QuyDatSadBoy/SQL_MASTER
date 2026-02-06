"""
Pydantic schemas for Office entity.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from decimal import Decimal
from datetime import date


class OfficeBase(BaseModel):
    """Base schema for Office."""
    name: str = Field(..., max_length=50, description="Tên/Mã phòng (P101, P102...)")
    area: Decimal = Field(..., gt=0, description="Diện tích (m2)")
    floor: int = Field(..., description="Tầng")
    position: Optional[str] = Field(None, max_length=100, description="Vị trí (Góc, Hành lang, View đẹp...)")
    base_price: Decimal = Field(..., gt=0, description="Giá thuê cơ bản")


class OfficeCreate(OfficeBase):
    """Schema for creating an Office."""
    pass


class OfficeUpdate(BaseModel):
    """Schema for updating an Office."""
    name: Optional[str] = Field(None, max_length=50)
    area: Optional[Decimal] = Field(None, gt=0)
    floor: Optional[int] = None
    position: Optional[str] = Field(None, max_length=100)
    base_price: Optional[Decimal] = Field(None, gt=0)


class Office(OfficeBase):
    """Schema for Office response."""
    id: int
    
    model_config = ConfigDict(from_attributes=True)
