#!usr/bin/python3
# models/subscriptions

from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, String
from sqlalchemy.orm import relationship
from db.db import Base

class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    topic = Column(String, index=True)

    user = relationship("User", back_populates="subscriptions")
