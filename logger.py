import logging
from logging.handlers import RotatingFileHandler
import os

def get_rotational_logger(name='app_logger', path='app.log', max_size=1024*1024, backups=5):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    handler = RotatingFileHandler(
        path, 
        maxBytes=max_size, 
        backupCount=backups
    )
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger

class LoggerProxy:
    """Dynamic wrapper to intercept logging calls."""
    def __init__(self, logger):
        self._logger = logger
    
    def __getattr__(self, name):
        if name in ['debug', 'info', 'warning', 'error', 'critical']:
            return getattr(self._logger, name)
        raise AttributeError(f'Logger does not support {name}')

# Usage initialization
log = LoggerProxy(get_rotational_logger())