from pydantic import BaseModel
from typing_extensions import Annotated

class UserBase(BaseModel):
    username: str
    email: str
    password:str
    

class UserDisplay(BaseModel):
    id: int
    username: str
    email:str

    class Config():
        from_attributes = True


class User(BaseModel):
    username: str
    class Config():
        from_attributes = True

    
class UserToken(BaseModel):
    id: int
    username: str
    email: str
    class Config():
        from_attributes = True