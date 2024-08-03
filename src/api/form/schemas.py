from pydantic import BaseModel, ConfigDict
from datetime import datetime


class FormPreferencesRequest(BaseModel):
    # user_id : university id (e.i: 105285)
    user_id_sender: int
    user_id_student_2: int | None
    user_id_student_3: int | None
    user_id_student_4: int | None
    answer_id: datetime
    topic_1: str
    topic_2: str
    topic_3: str


class FormPreferencesResponse(BaseModel):
    user_id: int
    answer_id: datetime
    topic_1: str
    topic_2: str
    topic_3: str

    model_config = ConfigDict(from_attributes=True)


class UserAnswerResponse(BaseModel):
    answer_id: datetime
    email: str
    topic_1: str
    topic_2: str
    topic_3: str

    model_config = ConfigDict(from_attributes=True)


class GroupAnswerResponse(BaseModel):
    answer_id: datetime
    students: list[str]
    topics: list[str]
