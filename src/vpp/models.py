from pydantic import BaseModel, Field
from typing import Optional

class Plant(BaseModel):
    id: int
    name: str
    max_capacity: float = Field(..., gt=0, description="Maximum power output in kW")
    min_capacity: float = Field(0, ge=0, description="Minimum power output in kW")
    status: Optional[str] = Field("idle", description="Current status: idle/running/down")

class DispatchRequest(BaseModel):
    demand: float = Field(..., gt=0, description="Total power demand to meet in kW")

class DispatchResponse(BaseModel):
    allocations: dict
    total_dispatched: float
    unmet_demand: float
