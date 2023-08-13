from pydantic import BaseModel
from datetime import datetime
from typing import Annotated

class ResponseBase(BaseModel):
    username: str
    text: str
    comment_id: int
    edited: Annotated[bool, False]

class ResponseDisplay(BaseModel):
    id: int
    text: str
    username: str
    edited: bool
    timestamp: datetime
    class Config():
        from_attributes = True