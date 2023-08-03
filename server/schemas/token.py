from pydantic import BaseModel
from typing import List, Annotated
from schemas.user import UserDisplay

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserDisplay


class TokenData(BaseModel):
    id: Annotated[int, None]
    usernam: Annotated[str, None]
    scopes: List[str] = []