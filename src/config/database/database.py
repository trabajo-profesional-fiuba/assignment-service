from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

from src.config.config import api_config
from src.config.logging import logger

from src.config.database.models import Base

# En Fast API lo mejor es tener solo una instancia del engine, y que ese es
# el encargado de crear las sessiones que luego se van a usar

# Database Configurations
database_url = api_config.database_url
pool_size = api_config.database_pool_size
pool_timeout = api_config.database_pool_timeout

print(database_url)

engine = create_engine(
    database_url, pool_size=pool_size, pool_timeout=pool_timeout, echo=True
)

def init_default_values():
    with open("src/config/database/set_default_category.sql", "r") as file:
        stm = file.read()

    if engine:
        with engine.connect() as connection:
            try:
                # Execute the SQL script
                sql = text(stm)
                connection.execute(sql)
                connection.commit()
                logger.info("SQL script executed successfully.")
            except Exception as e:
                logger.error(f"An error occurred: {e}")
    else:
        logger.warn("Database engine is not initialized.")


def create_tables():
    """
    Creates all tables in the database.
    """
    try:
        Base.metadata.create_all(bind=engine)
        init_default_values()
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
    if engine != None:
        Session = sessionmaker(bind=engine)
        yield Session
    else:
        yield None
