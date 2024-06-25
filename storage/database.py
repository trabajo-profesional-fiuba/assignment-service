import os
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from contextlib import contextmanager

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
        self.create_tables()

    @contextmanager
    def get_session(self):
        """
        Context manager to handle SQLAlchemy sessions.
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error during session: {e}")
            raise
        finally:
            session.close()

    def create_tables(self):
        """
        Creates all tables in the database.
        """
        Base.metadata.create_all(bind=self.engine)

    def get_db(self):
        with self.get_session() as session:
            return session

    def delete_all_records_from_table(self, model):
        """
        Delete all records from the specified table.
        """
        with self.get_session() as session:
            try:
                session.query(model).delete()
                print(f"All records deleted from {model.__tablename__}.")
            except Exception as e:
                print(f"Error deleting records: {e}")
                raise
