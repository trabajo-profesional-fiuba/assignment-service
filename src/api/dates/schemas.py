from pydantic import BaseModel, ConfigDict, RootModel
from typing import List, Optional
from datetime import datetime


class DateSlotRequest(BaseModel):
    start: datetime
    end: datetime


class DateSlotRequestList(RootModel):
    root: List[DateSlotRequest]

    def __iter__(self):
        return iter(self.root)

class DateSlotResponse(BaseModel):
    slot: datetime

    model_config = ConfigDict(from_attributes=True)


class DateSlotResponseList(RootModel):
    root: List[DateSlotResponse]

    def __iter__(self):
        return iter(self.root)