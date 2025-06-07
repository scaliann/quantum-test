from datetime import datetime
from pydantic import BaseModel


class Post(BaseModel):
    id: int
    title: str
    text: str
    created_at: datetime
