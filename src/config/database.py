from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src.config.config import get_configuration

Base = declarative_base()
config = get_configuration()

# En Fast API lo mejor es tener solo una instancia del engine, y que ese es
# el encargado de crear las sessiones que luego se van a usar

# Database Configurations
database_url = config.get("database_url")
pool_size = config.get("pool_size")
pool_timeout = config.get("pool_timeout")

engine = create_engine(
    database_url,
    pool_size=config.get("pool_size"),
    pool_timeout=config.get("pool_timeout"),
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
