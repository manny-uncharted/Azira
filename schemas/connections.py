#!usr/bin/python3
# schemas/connection

from pydantic import BaseModel
from datetime import datetime

class ConnectionBase(BaseModel):
    user_id: int

class ConnectionCreate(ConnectionBase):
    num_of_connections: int

class Connection(ConnectionBase):
    id: int
    connected_at: datetime
    disconnected_at: datetime | None

    class Config:
        orm_mode = True
