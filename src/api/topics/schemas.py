from typing import List
from pydantic import BaseModel, ConfigDict, Field, RootModel


# Category schemas
class SimpleCategory(BaseModel):
    """Represents a simple category with just a name"""

    name: str

    model_config = ConfigDict(from_attributes=True)


class CompleteCategoryResponse(SimpleCategory):
    """Represents a complete category with id and name"""

    id: int


# Topic schemas


class SimpleTopic(BaseModel):
    """Represents a simple topic with just a name"""

    name: str

    model_config = ConfigDict(from_attributes=True)


class TopicRequest(SimpleTopic):
    category: str


class TopicResponse(SimpleTopic):
    id: int
    category: SimpleCategory = Field(validation_alias="category")


class TopicList(RootModel):
    root: List[TopicResponse]

    def __iter__(self):
        return iter(self.root)
