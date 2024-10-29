from pydantic import BaseModel, ConfigDict, Field, RootModel
from typing import List
from src.api.topics.schemas import SimpleTopic
from src.api.users.schemas import UserResponse


class TutorPeriodResponse(BaseModel):
    """Cuatrimestre de un tutor en particular"""

    id: int
    period_id: str
    tutor_id: int
    capacity: int
    is_evaluator: bool

    model_config = ConfigDict(from_attributes=True)


class TutorPeriodWithTopicsResponse(TutorPeriodResponse):
    """Cuatrimestre de un tutor en particular con los temas de ese cuatrimestre"""

    topics: List[SimpleTopic] = Field(default=[], validation_alias="topics")


class TutorResponse(UserResponse):
    """Tutor con sus cuatrimestres dentro"""

    tutor_periods: List[TutorPeriodResponse] = Field(default=[])


class TutorResponseWithTopics(UserResponse):
    """Tutor con sus cuatrimestres  y temas dentro"""

    tutor_periods: List[TutorPeriodWithTopicsResponse] = Field(default=[])


class TutorList(RootModel):
    """Lista de tutores"""

    root: List[TutorResponse]

    def __iter__(self):
        return iter(self.root)


class TutorWithTopicsList(RootModel):
    """Lista de tutores con sus temas"""

    root: List[TutorResponseWithTopics]

    def __iter__(self):
        return iter(self.root)


class TutorRequest(BaseModel):
    """Request de un nuevo tutor"""

    id: int
    name: str
    last_name: str
    email: str
    period: str
    capacity: int


class TutorMessage(BaseModel):
    """Mensaje de un tutor para enviar por mail"""

    body: str
