from typing import List
from pydantic import BaseModel, ConfigDict, RootModel


class CategoryRequest(BaseModel):
    name: str


class CategoryResponse(CategoryRequest):
    name: str

    model_config = ConfigDict(from_attributes=True)


class TopicRequest(BaseModel):
    name: str
    category: str


class TopicResponse(BaseModel):
    id: int
    name: str
    category: str

    model_config = ConfigDict(from_attributes=True)


class TopicList(RootModel):
    root: List[TopicResponse]

    def __iter__(self):
        return iter(self.root)
