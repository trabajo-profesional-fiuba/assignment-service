from src.config.database import Base
from sqlalchemy import Column, String, Integer


class TutorModel(Base):

    __tablename__ = "tutors"

    dni = Column(Integer, primary_key=True)
    name = Column(String)
    last_name = Column(String)
    email = Column(String, index=True, unique=True)
    password = Column(String)
