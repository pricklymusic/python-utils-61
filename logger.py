import logging
from logging.handlers import RotatingFileHandler
import sys

def setup_logger(name: str, log_file: str = 'app.log') -> logging.Logger:
    """Factory for persistent rolling loggers with flavor."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
    )

    # Rotation logic: 5MB per file, keeping 3 backups
    handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=3
    )
    handler.setFormatter(formatter)

    # Stream handler for console visibility
    stream = logging.StreamHandler(sys.stdout)
    stream.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)
        logger.addHandler(stream)

    return logger

# Instantiate core log interface
app_logger = setup_logger('python-utils-61')