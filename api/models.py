from pydantic import BaseModel
from datetime import datetime


class TopicPreferencesItem(BaseModel):
    email: str
    email_student_group_2: str | None
    email_student_group_3: str | None
    email_student_group_4: str | None
    group_id: datetime
    topic1: str
    topic2: str
    topic3: str


class TopicPreferencesUpdatedItem(BaseModel):
    email_student_group_2: str | None
    email_student_group_3: str | None
    email_student_group_4: str | None
    group_id: datetime
    topic1: str
    topic2: str
    topic3: str
