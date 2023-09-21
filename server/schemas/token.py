from pydantic import BaseModel
from typing import List
from typing_extensions import Optional
from schemas.user import UserDisplay

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserDisplay


class TokenData(BaseModel):
    id: Optional[int]
    username: Optional[str]
    scopes: List[str] = []