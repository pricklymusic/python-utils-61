import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name: str = 'app_logger', log_file: str = 'app.log') -> logging.Logger:
    """Factory for quirky rotating loggers."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(process)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=1048576, 
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

# Dynamic singleton logger for project-wide use
utils_logger = setup_logger('python-utils-61')