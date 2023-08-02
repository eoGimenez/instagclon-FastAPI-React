from pydantic import BaseModel
from datetime import datetime
from typing import List
from schemas.user import User
from schemas.comment import CommentDisplay

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
    comments: List[CommentDisplay]
    class Config():
        from_attributes = True