#!usr/bin/python3
# models/tokens

from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, String
from sqlalchemy.orm import relationship
from db.db import Base

class Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    access_token = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="tokens")
