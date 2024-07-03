from pydantic import BaseModel
from datetime import datetime


class TopicPreferencesItem(BaseModel):
    email_sender: str
    email_student_2: str | None
    email_student_3: str | None
    email_student_4: str | None
    group_id: datetime
    topic_1: str
    topic_2: str
    topic_3: str


class TopicPreferencesUpdatedItem(BaseModel):
    email_student_2: str | None
    email_student_3: str | None
    email_student_4: str | None
    group_id: datetime
    topic_1: str
    topic_2: str
    topic_3: str


class TopicPreferencesResponse(BaseModel):
    email: str
    group_id: datetime
    topic_1: str
    topic_2: str
    topic_3: str


class TopicCategoryItem(BaseModel):
    name: str
