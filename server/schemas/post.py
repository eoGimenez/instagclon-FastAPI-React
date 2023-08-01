from pydantic import BaseModel
from datetime import datetime
from schemas.user import User

class PostBase(BaseModel):
    image_url: str
    caption: str
    author_id: int


class PostDisplay(BaseModel):
    id: int
    image_url: str
    caption: str
    timestamp: datetime
    author: User
    class Config():
        from_attributes = True