from pydantic import BaseModel
from datetime import datetime


class GroupFormRequest(BaseModel):
    # uid : university id (e.i: 105285)
    uid_sender: int
    uid_student_2: int | None
    uid_student_3: int | None
    uid_student_4: int | None
    group_id: datetime
    topic_1: str
    topic_2: str
    topic_3: str

class GroupFormResponse(BaseModel):
    uid: int
    group_id: datetime
    topic_1: str
    topic_2: str
    topic_3: str