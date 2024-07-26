from sqlalchemy import Column, String, Integer, Enum
from src.config.database import Base
from enum import Enum as PyEnum


class Role(PyEnum):
    STUDENT = 'student'
    TUTOR = 'tutor'
    ADMIN = 'admin'


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    last_name = Column(String)
    email = Column(String, index=True, unique=True)
    password = Column(String)
    rol = Column(Enum(Role))