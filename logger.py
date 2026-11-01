import logging
import os
from logging.handlers import RotatingFileHandler

def get_rotational_logger(name='dev_logger', log_file='app.log', max_bytes=1024*1024, backup_count=3):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(name)s | %(message)s')
        
        # Rotating handler setup
        handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Stream fallback
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
    
    return logger

class LoggerProxy:
    """A creative wrapper to inject dynamic log contexts"""
    def __init__(self, logger):
        self._logger = logger
    
    def __getattr__(self, name):
        func = getattr(self._logger, name)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

# Usage initialization
app_logger = get_rotational_logger()
logger = LoggerProxy(app_logger)