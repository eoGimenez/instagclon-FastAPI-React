from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    password:str
    

class UserDisplat(BaseModel):
    username: str
    email:str
