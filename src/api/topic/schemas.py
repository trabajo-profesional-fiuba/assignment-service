from pydantic import BaseModel
from datetime import datetime


class TopicPreferencesRequest(BaseModel):
    uid_sender: int
    uid_student_2: int | None
    uid_student_3: int | None
    uid_student_4: int | None
    group_id: datetime
    topic_1: str
    category_1: str
    topic_2: str
    category_2: str
    topic_3: str
    category_3: str


class TopicPreferencesResponse(BaseModel):
    uid: int
    group_id: datetime
    topic_1: str
    category_1: str
    topic_2: str
    category_2: str
    topic_3: str
    category_3: str


class TopicCategoryRequest(BaseModel):
    name: str


class TopicRequest(BaseModel):
    name: str
    category: str
