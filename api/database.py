import os
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()


class TopicPreferences(Base):
    __tablename__ = "topic_preferences"

    email = Column(String, primary_key=True, index=True)
    group_id = Column(DateTime)
    topic1 = Column(String)
    topic2 = Column(String)
    topic3 = Column(String)


class Database:
    """
    Database class that manages the database setup and sessions.
    """

    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def get_session(self):
        """
        Creates and returns a new SQLAlchemy session.
        """
        return self.SessionLocal()

    def create_tables(self):
        """
        Creates all tables in the database.
        """
        Base.metadata.create_all(bind=self.engine)

    def setup(self):
        self.create_tables()
        session = self.get_session()
        return session
