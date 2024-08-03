from typing import List
from pydantic import BaseModel, ConfigDict, Field, RootModel
from datetime import datetime
from src.api.users.schemas import UserResponse


class PeriodRequest(BaseModel):
    id: str


class PeriodResponse(BaseModel):
    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PeriodList(RootModel):
    root: List[PeriodResponse]

class TutorPeriodResponse(BaseModel):
    id: int
    period_id: str
    tutor_id: int
    capacity: int
    is_evaluator: bool

    model_config = ConfigDict(from_attributes=True)


class TutorResponse(UserResponse):
    periods: List[TutorPeriodResponse] = Field(default=[])

class TutorList(RootModel):
    root: List[TutorResponse]
    
    def __iter__(self):
        return iter(self.root)
