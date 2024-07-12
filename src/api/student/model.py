from src.config.database import Base
from sqlalchemy import Column, String

class StudentModel(Base):

    __tablename__ = "students"

    id = Column(String, primary_key=True)
    name = Column(String)
    last_name = Column(String)
    email = Column(String, index=True, unique=True)
    password = Column(String)
