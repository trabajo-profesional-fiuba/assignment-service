from pydantic import BaseModel, ConfigDict


class CategoryRequest(BaseModel):
    name: str


class CategoryResponse(CategoryRequest):
    name: str

    model_config = ConfigDict(from_attributes=True)


class TopicRequest(BaseModel):
    name: str
    category: str


class TopicResponse(BaseModel):
    name: str
    category: str

    model_config = ConfigDict(from_attributes=True)
