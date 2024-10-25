from datetime import datetime
from pydantic import BaseModel, ConfigDict, RootModel
from typing import List, Optional


class PeriodRequest(BaseModel):
    """Schema basico de un cuatrimestre"""

    id: str


class PeriodResponse(PeriodRequest):
    """Cuatrimestre completo con estados"""

    created_at: Optional[datetime] = None
    form_active: Optional[bool] = None
    initial_project_active: Optional[bool] = None
    intermediate_project_active: Optional[bool] = None
    final_project_active: Optional[bool] = None
    groups_assignment_completed: Optional[bool] = None
    topics_tutors_assignment_completed: Optional[bool] = None
    presentation_dates_assignment_completed: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class PeriodList(RootModel):
    """Lista de cuatrimestres"""

    root: List[PeriodResponse]


class UpdatePeriodRequest(PeriodRequest):
    """Schema para actualizar un cuatrimestre"""

    form_active: Optional[bool] = None
    initial_project_active: Optional[bool] = None
    intermediate_project_active: Optional[bool] = None
    final_project_active: Optional[bool] = None
    groups_assignment_completed: Optional[bool] = None
    topics_tutors_assignment_completed: Optional[bool] = None
    presentation_dates_assignment_completed: Optional[bool] = None
