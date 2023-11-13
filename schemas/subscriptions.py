#!usr/bin/python3
# schemas/subscriptions

from pydantic import BaseModel

class SubscriptionBase(BaseModel):
    user_id: int
    topic: str

class SubscriptionCreate(SubscriptionBase):
    pass

class Subscription(SubscriptionBase):
    id: int

    class Config:
        orm_mode = True
