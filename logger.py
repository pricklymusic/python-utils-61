import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name: str, log_path: str = "app.log") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s'
        )
        
        handler = RotatingFileHandler(
            log_path, 
            maxBytes=1024 * 1024 * 5, 
            backupCount=3
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
        
    return logger

log = get_logger("python-utils-61")