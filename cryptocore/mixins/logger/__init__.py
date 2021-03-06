import sys
import os
import logging

from .colored_logging import ColoredFormatter

from cryptocore.config import ENVIRONMENT, LOG_PATH

DEFAULT_LOGGING_LEVEL = logging.DEBUG if ENVIRONMENT == "development" else logging.INFO

_PATH = os.path.join(LOG_PATH, "{name}.log")
_FORMATTER = ColoredFormatter(
    "[%(name)s][%(levelname)s]: %(asctime)-15s %(location)s %(message)s", datefmt="%m-%d-%y-%I:%M:%S%p"
)

class CustomLogger(logging.Logger):
    def _log(self, level, msg, args, truncate=None, **kwargs):
        if truncate is not None:
            msg = msg[:truncate]
        return super()._log(level, msg, args, **kwargs)
     

logging.setLoggerClass(CustomLogger)
def set_logging_level(level):
    global DEFAULT_LOGGING_LEVEL
    DEFAULT_LOGGING_LEVEL = level


def configure_logger():
    # Default logging level to ERROR
    logging.getLogger().setLevel(logging.ERROR)
    logging.getLogger("requests").setLevel(logging.CRITICAL)
    logging.getLogger("urllib").setLevel(logging.CRITICAL)

    root = logging.getLogger("crypto")
    root.setLevel(DEFAULT_LOGGING_LEVEL)
    root.propagate = False

    # Error Logging
    errorHandler = logging.FileHandler(
        _PATH.format(name="crypto-errors")
    )
    errorHandler.setFormatter(_FORMATTER)
    errorHandler.setLevel(logging.WARNING)

    # STDOUT Logging - use supervisor to capture stdout
    stdout = logging.StreamHandler(sys.stdout)
    stdout.setFormatter(_FORMATTER)
    stdout.setLevel(DEFAULT_LOGGING_LEVEL)

    root.addHandler(errorHandler)
    root.addHandler(stdout)
    
    return root

ROOT_LOGGER = configure_logger()

# Debug logger for printouts
DEBUG_LOGGER = ROOT_LOGGER.getChild("debugger")
DEBUG_LOGGER.setLevel(logging.DEBUG)

def get_logger(name):
    handler = logging.FileHandler(
        _PATH.format(name="crypto-" + name)
    )
    handler.setFormatter(_FORMATTER)

    logger = ROOT_LOGGER.getChild(name)
    logger.addHandler(handler)

    return logger


class LoggerMixin(object):
    __logger_name__ = None

    def __init__(self, logger_name=None):
        logger_name = logger_name or self.__logger_name__
        
        if logger_name is None:
            raise ValueError("cls.__logger_name__ must be set, or logger_name must be provided in __init__")

        self.logger = get_logger(logger_name)
        
