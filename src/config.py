from pydantic import BaseModel

class LogConfig(BaseModel):
  """Logging configuration to be set for the server"""

  LOGGER_NAME: str = 'todoapp'
  LOG_FORMAT: str = '%(levelprefix)s | %(asctime)s | %(message)s'
  LOG_LEVEL: str = 'DEBUG'

  # Logging config
  version: int = 1
  disable_existing_loggers: bool = False
  formatters: dict[str, dict[str, str]] = {
    'default': {
      '()': 'uvicorn.logging.DefaultFormatter',
      'fmt': LOG_FORMAT,
      'datefmt': '%Y-%m-%d %H:%M:%S',
    },
  }
  handlers: dict[str, dict[str, str]] = {
    'default': {
      'formatter': 'default',
      'class': 'logging.StreamHandler',
      'stream': 'ext://sys.stderr',
    },
  }
  loggers: dict[str, dict[str, list | str]] = {
    LOGGER_NAME: {'handlers': ['default'], 'level': LOG_LEVEL},
  }
