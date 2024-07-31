from typing import List
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from src.api.users.schemas import UserResponse


class PeriodRequest(BaseModel):
    id: str


class PeriodResponse(BaseModel):
    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TutorPeriodResponse(BaseModel):
    id: int
    period_id: str
    tutor_id: int
    capacity: int
    is_evaluator: bool

    model_config = ConfigDict(from_attributes=True)


class TutorResponse(UserResponse):
    periods: List[TutorPeriodResponse] = Field(default=[])
