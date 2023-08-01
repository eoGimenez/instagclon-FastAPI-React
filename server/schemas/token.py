from pydantic import BaseModel
from typing import List
from schemas.user import UserDisplay

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserDisplay


class TokenData(BaseModel):
    id: int | None = None
    usernam: str | None = None
    scopes: List[str] = []