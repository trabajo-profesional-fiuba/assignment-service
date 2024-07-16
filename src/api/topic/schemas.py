from pydantic import BaseModel

class CategoryRequest(BaseModel):
    name: str

class CategoryResponse(CategoryRequest):
    id: int

    class Config:
        orm_mode = True


class TopicRequest(BaseModel):
    name: str
    category: str


class TopicReponse(TopicRequest):
    id: int

    class Config:
        orm_mode = True
