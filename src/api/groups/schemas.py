from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, RootModel, field_validator
from src.api.topics.schemas import TopicResponse
from src.api.users.schemas import UserResponse
from typing import List, Optional, Dict, Any


class GroupRequest(BaseModel):
    students_ids: List[int]

    @field_validator("students_ids", mode="before")
    def validate_group_length(cls, students_ids):
        if 0 < len(students_ids) <= 4:
            return students_ids

        raise ValueError("The amount of student for this Group is not valid")


class GroupWithTutorTopicRequest(GroupRequest):
    tutor_email: str
    topic: str


class AssignedGroupConfirmationRequest(BaseModel):
    id: int
    tutor_period_id: Optional[int] = None
    assigned_topic_id: Optional[int] = None
    reviewer_id: Optional[int] = None
    pre_report_approved: Optional[bool] = None
    intermediate_assigment_approved: Optional[bool] = None
    final_report_approved: Optional[bool] = None


class AssignedGroupResponse(BaseModel):
    id: int
    tutor: Dict[str, Any]
    topic: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)


class AssignedDateSlotResponse(BaseModel):
    group_id: int
    tutor_id: int
    evaluator_id: int
    date: datetime
    spanish_date: str

    model_config = ConfigDict(from_attributes=True)


class AssignedDateResult(BaseModel):
    status: int
    assigments: list[AssignedDateSlotResponse]


class GroupWithPreferredTopicsRequest(GroupRequest):
    preferred_topics: List[int]


class GroupResponse(BaseModel):
    id: int = Field(description="Id of the group")
    students: List[UserResponse] = Field(default=[])
    period_id: str
    # topic_id: int | None = Field(validation_alias="assigned_topic_id")
    tutor_period_id: int | None = Field(validation_alias="tutor_period_id")
    preferred_topics: Optional[List[int]] = Field(
        description="Ids of topics the group selected in the form answer"
    )
    topic: Optional[TopicResponse]
    reviewer_id: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class GroupStates(BaseModel):
    pre_report_date: datetime | None
    pre_report_approved: bool
    pre_report_title: str | None
    intermediate_assigment_date: datetime | None
    intermediate_assigment_approved: bool
    intermediate_assigment: str | None
    final_report_approved: bool
    final_report_title: str | None
    final_report_date: datetime | None
    exhibition_date: datetime | None

    model_config = ConfigDict(from_attributes=True)


class CompleteGroupResponse(GroupResponse, GroupStates): ...


class GroupList(RootModel):
    root: List[GroupResponse] = Field(default=[])


class GroupStatesList(RootModel):
    root: List[GroupStates] = Field(default=[])


class GroupCompleteList(RootModel):
    root: List[CompleteGroupResponse] = Field(default=[])


class AssignmentResult(BaseModel):
    status: int
    assigment: List[AssignedGroupResponse] = Field(default=[])
    dcg: Optional[float]


class BlobDetails(BaseModel):
    name: str
    created_on: datetime
    last_modified: datetime
    container: str


class BlobDetailsList(RootModel):
    root: List[BlobDetails] = Field(default=[])


class IntermediateAssignmentRequest(BaseModel):
    url: str
