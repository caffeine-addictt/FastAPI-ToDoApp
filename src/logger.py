import logging
from logging.config import dictConfig

from .config import LogConfig

# Logging setup
dictConfig(LogConfig().model_dump())
logger = logging.getLogger('todoapp')
