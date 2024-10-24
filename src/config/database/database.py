from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from src.config.config import api_config
from src.config.database.models import Base
from src.config.logging import logger

# Solo debemos tener un engine y manejarnos con Sessions

# Database Configurations desde la clase de configuracion
database_url = api_config.database_url
pool_size = api_config.database_pool_size
pool_timeout = api_config.database_pool_timeout

# pool_pre_ping se asegura de que cuando se crea la instancia del engine, esta responda
# porque sino por default, sqlalchemy tiene operaciones lazy
engine = create_engine(
    database_url, pool_size=pool_size, pool_timeout=pool_timeout, pool_pre_ping=True
)


def init_default_values():
    """Inserta valores defaults"""
    with open("src/config/database/init.sql", "r") as file:
        stm = file.read()

    if engine:
        with engine.connect() as connection:
            try:
                sql = text(stm)
                connection.execute(sql)
                connection.commit()
                logger.info("Default values executed successfully.")
            except Exception as e:
                logger.error(f"An error occurred: {e}")
    else:
        logger.warning("Database engine is not initialized.")


#NOTE - Como manejamos migraciones, esta funcion solo debe ser llamada para tests
def create_tables():
    """Crea todas las tablas"""
    try:
        logger.info("Creating all the tables")
        Base.metadata.create_all(bind=engine)
        init_default_values()
    except Exception as err:
        logger.error("An error ocurred during the table creation")
        raise err

#NOTE - Como manejamos migraciones, esta funcion solo debe ser llamada para tests
def drop_tables():
    """Borra todas las tablas"""
    try:
        Base.metadata.drop_all(bind=engine)
    except Exception as err:
        raise err


def get_db():
    """Retorna una instancia de una session haciendo un yield"""
    if engine is not None:
        Session = sessionmaker(bind=engine)
        yield Session
    else:
        yield None
