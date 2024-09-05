import logging
from src.config.config import api_config


# Formatter
formatter = logging.Formatter()

# Handler
stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(api_config.logging_level)
stdout_handler.setFormatter(formatter)

# Logger
logger = logging.getLogger(__name__)
logger.setLevel(api_config.logging_level)  # Set the logging level for the logger itself
logger.addHandler(stdout_handler)

# sql alchemy logger configuration
sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
sqlalchemy_logger.setLevel(logging.DEBUG)
sqlalchemy_logger.addHandler(stdout_handler)

# Optional: Prevent propagation of log messages to ancestor loggers
logger.propagate = False
