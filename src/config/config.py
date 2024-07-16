import os
from dotenv import load_dotenv

def get_configuration():
    database_url = os.getenv("DATABASE_URL", None)
    pool_size =  os.getenv("DATABASE_POOL_SIZE", 10)
    pool_timeout =  os.getenv("DATABASE_TIMEOUT", 10)

    config = {
        "database_url": database_url,
        "pool_size": pool_size,
        "pool_timeout": pool_timeout
    }

    return config