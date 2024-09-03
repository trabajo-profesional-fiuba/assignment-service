import logging
from src.config.config import api_config


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    green = "\x1b[32m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# Formatter
formatter = CustomFormatter()

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
sqlalchemy_logger.setLevel(logging.WARN)
sqlalchemy_logger.addHandler(stdout_handler)

# Optional: Prevent propagation of log messages to ancestor loggers
logger.propagate = False
