from pydantic import BaseModel
from datetime import datetime

class CommentBase(BaseModel):
    username: str
    text: str
    post_id: int

class CommentDisplay(BaseModel):
    text: str
    username: str
    timestamp: datetime
    class Config():
        from_attributes = True