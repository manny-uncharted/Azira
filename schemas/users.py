#!usr/bin/python3
# schemas/users
from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True
