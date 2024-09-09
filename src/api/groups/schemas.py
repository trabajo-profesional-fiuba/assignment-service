from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, RootModel, field_validator
from src.api.users.schemas import UserResponse
from typing import List, Optional


class GroupRequest(BaseModel):
    students_ids: List[int]
    tutor_email: Optional[str] = None
    topic: Optional[str] = None
    preferred_topics: Optional[List[int]] = None

    @field_validator("students_ids", mode="before")
    def validate_group_length(cls, students_ids):
        if 0 < len(students_ids) <= 4:
            return students_ids

        raise ValueError("The amount of student for this Group is not valid")


class GroupResponse(BaseModel):

    id: int = Field(description="Id of the group")
    topic_id: int | None = Field(validation_alias="assigned_topic_id")
    tutor_period_id: int | None = Field(validation_alias="tutor_period_id")
    pre_report_date: datetime | None
    pre_report_approved: bool
    intermediate_assigment_date: datetime | None
    intermediate_assigment_approved: bool
    final_report_approved: bool
    exhibition_date: datetime | None
    preferred_topics: List[int] = Field(
        description="Ids of topics the group selected in the form answer"
    )
    students: List[UserResponse] = Field(default=[])
    period_id: str
    
    model_config = ConfigDict(from_attributes=True)


class GroupList(RootModel):
    root: List[GroupResponse] = Field(default=[])
