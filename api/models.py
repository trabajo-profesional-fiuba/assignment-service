from pydantic import BaseModel
from datetime import datetime


class TopicPreferencesItem(BaseModel):
    email: str
    group_id: datetime
    topic1: str
    topic2: str
    topic3: str
