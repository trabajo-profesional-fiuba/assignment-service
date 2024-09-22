from pydantic import BaseModel, ConfigDict, RootModel
from typing import List, Optional
from datetime import datetime


class PeriodRequest(BaseModel):
    id: str


class PeriodResponse(PeriodRequest):
    created_at: Optional[datetime] = None
    form_active: Optional[bool] = None
    initial_project_active: Optional[bool] = None
    intermediate_project_active: Optional[bool] = None
    final_project_active: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class PeriodList(RootModel):
    """List of Period"""

    root: List[PeriodResponse]


class UpdatePeriodRequest(PeriodRequest):
    form_active: Optional[bool] = None
    initial_project_active: Optional[bool] = None
    intermediate_project_active: Optional[bool] = None
    final_project_active: Optional[bool] = None
