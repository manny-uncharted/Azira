#!usr/bin/python3
# models/connections

from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from db.db import Base

class Connection(Base):
    __tablename__ = 'connections'

    id = Column(Integer, primary_key=True, index=True)
    number_of_connections = Column(Integer, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    connected_at = Column(DateTime(timezone=True), server_default=func.now())
    disconnected_at = Column(DateTime(timezone=True))

    user = relationship("User", back_populates="connections")
