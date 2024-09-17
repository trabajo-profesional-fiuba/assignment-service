from pydantic import BaseModel, ConfigDict, Field, RootModel
from typing import List
from src.api.topics.schemas import SimpleTopic
from src.api.users.schemas import UserResponse


class TutorPeriodResponse(BaseModel):
    """Period of tutor"""

    id: int
    period_id: str
    tutor_id: int
    capacity: int
    is_evaluator: bool

    model_config = ConfigDict(from_attributes=True)


class TutorPeriodWithTopicsResponse(TutorPeriodResponse):
    """Period of tutor with its topics, just showing the name"""

    topics: List[SimpleTopic] = Field(default=[], validation_alias="topics")


class TutorResponse(UserResponse):
    """Tutor representation with the periods inside"""

    tutor_periods: List[TutorPeriodResponse] = Field(default=[])


class TutorResponseWithTopics(UserResponse):
    """Tutor representation with the periods inside"""

    tutor_periods: List[TutorPeriodWithTopicsResponse] = Field(default=[])


class TutorList(RootModel):
    """Default list of tutors"""

    root: List[TutorResponse]

    def __iter__(self):
        return iter(self.root)


class TutorWithTopicsList(RootModel):
    """List of tutors and their topics"""

    root: List[TutorResponseWithTopics]

    def __iter__(self):
        return iter(self.root)

class TutorRequest(BaseModel):
    id: int
    name: str
    last_name: str
    email: str
    period: str
    capacity: int