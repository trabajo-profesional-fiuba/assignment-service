from pydantic import BaseModel, ConfigDict
from datetime import datetime


class PeriodRequest(BaseModel):
    id: str


class PeriodResponse(BaseModel):
    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TutorPeriodResponse(BaseModel):
    id: str
    tutor_id: int
    capacity : int
    is_evaluator : bool

    model_config = ConfigDict(from_attributes=True)
