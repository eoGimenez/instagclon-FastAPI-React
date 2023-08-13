from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from schemas.user import User

class ResponseBase(BaseModel):
    username: str
    text: str
    comment_id: int
    edited: Optional[bool] | None = False

class ResponseDisplay(BaseModel):
    id: int
    text: str
    username: str
    edited: bool
    author_id: int
    author_response: User
    timestamp: datetime
    class Config():
        from_attributes = True