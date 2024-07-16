from src.config.database import Base
from sqlalchemy import Column, String, Integer

class StudentModel(Base):

    __tablename__ = "students"

    uid = Column(Integer, primary_key=True)
    name = Column(String)
    last_name = Column(String)
    email = Column(String,)
    password = Column(String)
