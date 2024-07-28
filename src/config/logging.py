import logging
from src.config.config import api_config

# Formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")

# Handler
stdoutHandler = logging.StreamHandler()
stdoutHandler.setLevel(api_config.logging_level)
stdoutHandler.setFormatter(formatter)

# Logger
logger = logging.getLogger(__name__)
logger.setLevel(api_config.logging_level)  # Set the logging level for the logger itself
logger.addHandler(stdoutHandler)

# Optional: Prevent propagation of log messages to ancestor loggers
logger.propagate = False
