import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name='app_logger', log_file='app.log', max_bytes=1048576, backup_count=3):
    """Factory function for creating quirky rotating loggers."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(process)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=max_bytes, 
            backupCount=backup_count
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Add a stream handler for console visibility
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
        
    return logger

# Instantiate a singleton-like logger for the utility
log = get_logger('python-utils-61')