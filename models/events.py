#!usr/bin/python3
# models/events

from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, String
from sqlalchemy.orm import relationship
from db.db import Base

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    event_type = Column(String)
    details = Column(String)  # JSON or text detailing the event
    occurred_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="events")
