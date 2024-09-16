from pydantic import BaseModel, ConfigDict, RootModel
from typing import List
from datetime import datetime


class PeriodRequest(BaseModel):
    id: str


class PeriodResponse(PeriodRequest):
    created_at: datetime
    form_active: bool
    initial_project_active: bool
    intermediate_project_active: bool
    final_project_active: bool

    model_config = ConfigDict(from_attributes=True)


class PeriodList(RootModel):
    """List of Period"""

    root: List[PeriodResponse]
