from datetime import datetime
from pydantic import BaseModel, ConfigDict, RootModel
from typing import List


class FormPreferencesRequest(BaseModel):
    """Representa el formulario que los alumnos envian"""

    user_id_sender: int
    user_id_student_2: int | None
    user_id_student_3: int | None
    user_id_student_4: int | None
    answer_id: datetime
    topic_1: str
    topic_2: str
    topic_3: str


class FormPreferencesResponse(BaseModel):
    """Schema de respuesta particular de un estudiante"""

    user_id: int
    answer_id: datetime
    topic_1: str
    topic_2: str
    topic_3: str

    model_config = ConfigDict(from_attributes=True)


class FormPreferencesList(RootModel):
    """Lista de respuestas"""

    root: List[FormPreferencesResponse]

    def __iter__(self):
        return iter(self.root)


class GroupAnswerResponse(BaseModel):
    """Respuestas de un grupo"""

    id: datetime
    students: list[str]
    topics: list[str]


class GroupAnswerList(RootModel):
    """Lista de respuestas de un grupo"""

    root: List[GroupAnswerResponse]

    def __iter__(self):
        return iter(self.root)
