import uvicorn
from src.config.config import api_config
from src.config.logging import logger

if __name__ == "__main__":
    host = api_config.host
    port = api_config.port
    workers = api_config.workers

    logger.warning(f"Server listening at host: {host}")
    logger.warning(f"Server listening at port: {port}")
    logger.warning(f"Server running with workers: {workers}")


    try:
        uvicorn.run("src.api.app:app", host=host, port=port,workers=workers )
    except KeyboardInterrupt:
        logger.warning("Server stopped mannualy")
