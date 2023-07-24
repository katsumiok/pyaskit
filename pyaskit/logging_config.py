import os
import logging


def setup_logger(logger_name):
    log_level = os.getenv("ASKIT_LOG_LEVEL", "WARNING").upper()
    numeric_level = getattr(logging, log_level, None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")
    logger = logging.getLogger(logger_name)
    logger.setLevel(numeric_level)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)  # set handler level
    logger.addHandler(ch)

    return logger
