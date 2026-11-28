import logging
from logging.handlers import RotatingFileHandler
import os

def get_rotating_logger(name='app_logger', log_file='app.log', level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        handler = RotatingFileHandler(
            log_file,
            maxBytes=1024 * 1024 * 5,
            backupCount=3,
            encoding='utf-8'
        )
        
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
    
    return logger

# Dynamic wrapper for quick debugging
class DebugLogger:
    def __init__(self, name='dev'):
        self.logger = get_rotating_logger(name)

    def __getattr__(self, attr):
        return getattr(self.logger, attr)

logger = DebugLogger()