from pydantic import BaseModel, ConfigDict


class CategoryRequest(BaseModel):
    name: str


class CategoryResponse(CategoryRequest):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TopicRequest(BaseModel):
    name: str
    category: str


class TopicReponse(BaseModel):
    id: int
    name: str
    category_id: int

    model_config = ConfigDict(from_attributes=True)
