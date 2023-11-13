#! usr/bin/python3
# models/users

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    tokens = relationship("Token", back_populates="user", uselist=False)