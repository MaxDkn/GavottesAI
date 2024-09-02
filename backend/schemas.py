# schemas.py
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True
