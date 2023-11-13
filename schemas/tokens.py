#!usr/bin/python3
# schemas/tokens.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TokenBase(BaseModel):
    access_token: str

class TokenCreate(TokenBase):
    pass

class Token(TokenBase):
    id: int
    user_id: int
    created_at: datetime
