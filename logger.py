import logging
from logging.handlers import RotatingFileHandler
import os

def get_rotating_logger(name='app_logger', log_file='app.log', max_bytes=1024*1024, backup_count=3):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=max_bytes, 
            backupCount=backup_count
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
        
    return logger

class LoggerContext:
    def __init__(self, name, filename):
        self.name = name
        self.filename = filename
    def __enter__(self):
        return get_rotating_logger(self.name, self.filename)
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass