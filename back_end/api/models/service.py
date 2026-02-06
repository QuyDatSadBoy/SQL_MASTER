"""
Pydantic schemas for Service entity.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from decimal import Decimal


class ServiceBase(BaseModel):
    """Base schema for Service."""
    name: str = Field(..., max_length=100, description="Vệ sinh, An ninh, Gửi xe...")
    description: Optional[str] = None
    base_price: Optional[Decimal] = Field(None, description="Giá cơ bản")
    price_method: Optional[str] = Field(None, max_length=50, description="per_sqm, per_head, fixed...")


class ServiceCreate(ServiceBase):
    """Schema for creating a Service."""
    pass


class ServiceUpdate(BaseModel):
    """Schema for updating a Service."""
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    base_price: Optional[Decimal] = None
    price_method: Optional[str] = Field(None, max_length=50)


class Service(ServiceBase):
    """Schema for Service response."""
    id: int
    
    model_config = ConfigDict(from_attributes=True)
