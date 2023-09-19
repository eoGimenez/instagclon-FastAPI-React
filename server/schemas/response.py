from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from schemas.user import User

class ResponseBase(BaseModel):
    username: str
    text: str
    comment_id: int
    author_id: int

class ResponsePost(BaseModel):
    username: str
    text: str
    author_id: int

class ResponseDisplay(BaseModel):
    id: int
    text: str
    username: str
    edited: bool
    timestamp: datetime
    author_response: User
    class Config():
        from_attributes = True