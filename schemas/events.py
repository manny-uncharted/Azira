#!usr/bin/python3
# schemas/events

from pydantic import BaseModel
from datetime import datetime

class EventBase(BaseModel):
    user_id: int
    event_type: str
    details: str

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    occurred_at: datetime

    class Config:
        orm_mode = True
