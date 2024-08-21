from typing import List
from pydantic import BaseModel, ConfigDict, Field, RootModel


class SimpleCategory(BaseModel):
    """ Represents a simple category with just a name"""
    name: str
class CategoryResponse(SimpleCategory):
    """Can validate models from Categories"""
    model_config = ConfigDict(from_attributes=True)

class CompleteCategoryResponse(SimpleCategory):
    """ Represents a complete category with id and name"""
    id: int

    model_config = ConfigDict(from_attributes=True)

class TopicRequest(BaseModel):
    name: str
    category: str


class TopicResponse(BaseModel):
    id: int
    name: str
    category: CategoryResponse = Field(validation_alias='category')

    model_config = ConfigDict(from_attributes=True)


class TopicList(RootModel):
    root: List[TopicResponse]

    def __iter__(self):
        return iter(self.root)
