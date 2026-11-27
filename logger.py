import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name='python-utils-61', log_file='app.log', max_bytes=1048576, backup_count=3):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    if not logger.handlers:
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=max_bytes, 
            backupCount=backup_count
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

log = setup_logger()

def log_debug(msg):
    log.debug(msg)

def log_error(msg):
    log.error(msg)