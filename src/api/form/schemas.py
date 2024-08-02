from pydantic import BaseModel, ConfigDict
from datetime import datetime


class FormPreferencesRequest(BaseModel):
    # uid : university id (e.i: 105285)
    uid_sender: int
    uid_student_2: int | None
    uid_student_3: int | None
    uid_student_4: int | None
    answer_id: datetime
    topic_1: str
    topic_2: str
    topic_3: str


class FormPreferencesResponse(BaseModel):
    uid: int
    answer_id: datetime
    topic_1: str
    topic_2: str
    topic_3: str

    model_config = ConfigDict(from_attributes=True)
