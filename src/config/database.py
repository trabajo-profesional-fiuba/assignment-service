from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src.config.config import api_config

Base = declarative_base()


# En Fast API lo mejor es tener solo una instancia del engine, y que ese es
# el encargado de crear las sessiones que luego se van a usar

# Database Configurations
database_url = api_config.database_url
pool_size = api_config.database_pool_size
pool_timeout = api_config.database_pool_timeout

engine = create_engine(
    database_url,
    pool_size=pool_size,
    pool_timeout=pool_timeout,
    echo=True
)


def create_tables():
    """
    Creates all tables in the database.
    """
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as err:
        raise err


def drop_tables():
    """
    Drop all tables in the database.
    """
    try:
        Base.metadata.drop_all(bind=engine)
    except Exception as err:
        raise err


def get_db():
    Session = sessionmaker(bind=engine)
    yield Session
