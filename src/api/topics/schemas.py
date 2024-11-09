from typing import List
from pydantic import BaseModel, ConfigDict, Field, RootModel


# Category schemas
class SimpleCategory(BaseModel):
    """Representa una categoria con solo su nombre"""

    name: str

    model_config = ConfigDict(from_attributes=True)


class CompleteCategoryResponse(SimpleCategory):
    """Representa una categoria completa"""

    id: int


# Topic schemas


class SimpleTopic(BaseModel):
    """Representa un tema simple"""

    name: str

    model_config = ConfigDict(from_attributes=True)


class TopicRequest(SimpleTopic):
    """Representa un tema completo"""

    category: str
    tutor_email: str
    capacity: int | None = Field(default=1)


class TopicResponse(SimpleTopic):
    """Representa una respuesta de un tema"""

    id: int
    category: SimpleCategory = Field(validation_alias="category")


class TopicList(RootModel):
    """Representa una lista de temas"""

    root: List[TopicResponse]

    def __iter__(self):
        return iter(self.root)
