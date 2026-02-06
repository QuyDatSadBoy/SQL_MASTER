"""
Pydantic schemas for SalaryRule entity.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class SalaryRuleBase(BaseModel):
    """Base schema for SalaryRule."""
    bonus_rate: Optional[float] = Field(None, description="Hệ số thưởng/tỉ lệ % theo doanh thu")
    status: Optional[str] = Field(None, max_length=20)


class SalaryRuleCreate(SalaryRuleBase):
    """Schema for creating a SalaryRule."""
    pass


class SalaryRuleUpdate(BaseModel):
    """Schema for updating a SalaryRule."""
    bonus_rate: Optional[float] = None
    status: Optional[str] = Field(None, max_length=20)


class SalaryRule(SalaryRuleBase):
    """Schema for SalaryRule response."""
    id: int
    
    model_config = ConfigDict(from_attributes=True)
