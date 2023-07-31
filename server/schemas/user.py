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
