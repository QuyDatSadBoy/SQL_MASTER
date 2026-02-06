"""
Pydantic schemas for ServiceRoleRule entity.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class ServiceRoleRuleBase(BaseModel):
    """Base schema for ServiceRoleRule."""
    service_id: int = Field(..., description="ID dịch vụ")
    role: str = Field(..., max_length=50, description="staff, manager, supervisor")
    salary_rule_id: int = Field(..., description="ID quy tắc lương")


class ServiceRoleRuleCreate(ServiceRoleRuleBase):
    """Schema for creating a ServiceRoleRule."""
    pass


class ServiceRoleRuleUpdate(BaseModel):
    """Schema for updating a ServiceRoleRule."""
    service_id: Optional[int] = None
    role: Optional[str] = Field(None, max_length=50)
    salary_rule_id: Optional[int] = None


class ServiceRoleRule(ServiceRoleRuleBase):
    """Schema for ServiceRoleRule response."""
    id: int
    
    model_config = ConfigDict(from_attributes=True)
