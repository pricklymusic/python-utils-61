import logging
import os
from logging.handlers import RotatingFileHandler

def get_logger(name: str = 'app_logger', log_file: str = 'app.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
        )
        
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=1048576,
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger

log = get_logger()