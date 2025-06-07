from datetime import datetime
from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    text: str


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
