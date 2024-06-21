import os
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class TopicPreferences(Base):
    __tablename__ = "topic_preferences"

    email = Column(String, primary_key=True, index=True)
    group_id = Column(DateTime)
    topic1 = Column(String)
    topic2 = Column(String)
    topic3 = Column(String)


Base.metadata.create_all(bind=engine)
