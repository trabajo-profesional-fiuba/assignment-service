import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from storage.tables import Base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@db:5432/postgres"
)


class Database:
    """
    Database class that manages the database setup and sessions.
    """

    def __init__(self):
        try:
            self.engine = create_engine(DATABASE_URL)
            self.SessionLocal = sessionmaker(bind=self.engine)
            self.drop_tables()
            self.create_tables()
        except Exception as err:
            raise err

    @contextmanager
    def get_session(self):
        """
        Context manager to handle SQLAlchemy sessions.
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as err:
            session.rollback()
            raise err
        finally:
            session.close()

    def create_tables(self):
        """
        Creates all tables in the database.
        """
        try:
            Base.metadata.create_all(bind=self.engine)
        except Exception as err:
            raise err

    def drop_tables(self):
        """
        Drop all tables in the database.
        """
        try:
            Base.metadata.drop_all(bind=self.engine)
        except Exception as err:
            raise err

    def get_db(self):
        with self.get_session() as session:
            return session
