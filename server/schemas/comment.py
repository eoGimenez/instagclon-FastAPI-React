from pydantic import BaseModel
from datetime import datetime
from typing import List
from schemas.response import ResponseDisplay
from schemas.user import User



class CommentBase(BaseModel):
    username: str
    text: str
    post_id: int
    author_id: int

class CommentDisplay(BaseModel):
    id: int
    text: str
    username: str
    edited: bool
    timestamp: datetime
    responses: List[ResponseDisplay]
    author_comment: User
    class Config():
        from_attributes = True