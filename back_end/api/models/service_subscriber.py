"""
Pydantic schemas for ServiceSubscriber entity.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date


class ServiceSubscriberBase(BaseModel):
    """Base schema for ServiceSubscriber."""
    service_id: int = Field(..., description="ID dịch vụ")
    employee_id: int = Field(..., description="ID nhân viên tòa nhà")
    service_role_rules_id: int = Field(..., description="ID quy tắc vai trò-dịch vụ")
    from_date: date = Field(..., description="Ngày bắt đầu làm dịch vụ")
    end_date: Optional[date] = Field(None, description="Ngày kết thúc")
    invoice_id: Optional[int] = Field(None, description="Hóa đơn lương (nếu trả theo đợt)")


class ServiceSubscriberCreate(ServiceSubscriberBase):
    """Schema for creating a ServiceSubscriber."""
    pass


class ServiceSubscriberUpdate(BaseModel):
    """Schema for updating a ServiceSubscriber."""
    service_id: Optional[int] = None
    employee_id: Optional[int] = None
    service_role_rules_id: Optional[int] = None
    from_date: Optional[date] = None
    end_date: Optional[date] = None
    invoice_id: Optional[int] = None


class ServiceSubscriber(ServiceSubscriberBase):
    """Schema for ServiceSubscriber response."""
    id: int
    
    model_config = ConfigDict(from_attributes=True)
