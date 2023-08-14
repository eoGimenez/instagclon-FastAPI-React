from pydantic import BaseModel
from typing_extensions import Optional

class UserBase(BaseModel):
    username: str
    email: str
    password:str
    avatar: Optional[str] | None = None

class UserSignUp(BaseModel):
    username: str
    email: str
    password:str
    re_password:str
    avatar: Optional[str] | None = None
    

class UserDisplay(BaseModel):
    id: int
    username: str
    email:str
    avatar: str

    class Config():
        from_attributes = True


class User(BaseModel):
    id: int
    username: str
    avatar: str
    active: bool
    class Config():
        from_attributes = True

    
class UserToken(BaseModel):
    id: int
    username: str
    email: str
    class Config():
        from_attributes = True