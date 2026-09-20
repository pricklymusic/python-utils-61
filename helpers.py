import logging
from logging.handlers import RotatingFileHandler
import os

def setup_rotating_logger(name: str, log_file: str = 'app.log', level: int = logging.INFO) -> logging.Logger:
    """
    custom rotating logger factory for python-utils-61
    wraps standard handlers in a clean functional interface
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # ensure log directory existence
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # rotation logic: 5mb per file, keep 3 backups
    handler = RotatingFileHandler(
        log_file, 
        maxBytes=5 * 1024 * 1024, 
        backupCount=3
    )
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)
    
    return logger