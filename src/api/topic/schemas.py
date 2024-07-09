from pydantic import BaseModel
from datetime import datetime


class TopicPreferencesSchema(BaseModel):
    email_sender: str
    email_student_2: str | None
    email_student_3: str | None
    email_student_4: str | None
    group_id: datetime
    topic_1: str
    category_1: str
    topic_2: str
    category_2: str
    topic_3: str
    category_3: str


class TopicPreferencesResponse(BaseModel):
    email: str
    group_id: datetime
    topic_1: str
    category_1: str
    topic_2: str
    category_2: str
    topic_3: str
    category_3: str


class TopicCategorySchema(BaseModel):
    name: str


class TopicSchema(BaseModel):
    name: str
    category: str
