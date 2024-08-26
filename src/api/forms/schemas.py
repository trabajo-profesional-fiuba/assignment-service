from typing import List
from pydantic import BaseModel, ConfigDict, RootModel
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


class FormPreferencesList(RootModel):
    root: List[FormPreferencesResponse]

    def __iter__(self):
        return iter(self.root)


class UserAnswerResponse(BaseModel):
    answer_id: datetime
    email: str
    topic_1: str
    topic_2: str
    topic_3: str

    model_config = ConfigDict(from_attributes=True)


class UserAnswerList(RootModel):
    root: List[UserAnswerResponse]

    def __iter__(self):
        return iter(self.root)


class GroupAnswerResponse(BaseModel):
    id: datetime
    students: list[str]
    topics: list[str]


class GroupAnswerList(RootModel):
    root: List[GroupAnswerResponse]

    def __iter__(self):
        return iter(self.root)
