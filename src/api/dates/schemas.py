from datetime import datetime
from pydantic import BaseModel, ConfigDict, RootModel
from typing import List


class DateSlotRequest(BaseModel):
    """Schema para los slots como entrada de datos"""

    start: datetime
    end: datetime


class DateSlotRequestList(RootModel):
    """Schema para lista de slots de entrada"""

    root: List[DateSlotRequest]

    def __iter__(self):
        return iter(self.root)


class DateSlotResponse(BaseModel):
    """Schema para los slots como salida de datos"""

    slot: datetime

    model_config = ConfigDict(from_attributes=True)


class DateSlotResponseList(RootModel):
    """Schema para listar los slots de salida"""

    root: List[DateSlotResponse]

    def __iter__(self):
        return iter(self.root)
