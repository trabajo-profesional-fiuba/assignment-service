from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager
from src.config.config import get_configuration

Base = declarative_base()
config = get_configuration()


class Database:
    """
    Database class that manages the database setup and sessions.
    """

    def __init__(self):
        try:
            database_url = config.get("database_url")
            if database_url:
                self.engine = create_engine(
                    database_url,
                    pool_size=config.get("pool_size"),  # Max number of connections
                    pool_timeout=config.get("pool_timeout"),  # Time until a connection fails
                )
                self.Session = sessionmaker(bind=self.engine)
            else:
                raise Exception("database_url not found.")
        except Exception as err:
            raise err

    def get_session(self):
        return self.Session()

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
