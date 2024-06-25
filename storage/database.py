import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()


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

    def delete_all_records_from_table(self, session, model):
        """
        Delete all records from the specified table.
        """
        try:
            session.query(model).delete()
            session.commit()
            print(f"All records deleted from {model.__tablename__}.")
        except Exception as e:
            session.rollback()
            print(f"Error deleting records: {e}")
        finally:
            session.close()
