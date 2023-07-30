from pydantic import BaseModel
from typing import List

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    usernam: str | None = None
    scopes: List[str] = []