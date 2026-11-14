import logging
from logging.handlers import RotatingFileHandler
import os

def get_rotating_logger(name, log_file='app.log', max_bytes=1048576, backups=3):
    """Generates a logger with rotation based on size."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=max_bytes, 
            backupCount=backups
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
    
    return logger

# Dynamic instantiation for internal modules
if __name__ == '__main__':
    log = get_rotating_logger('dev_logger')
    log.info('System initialized with rotation strategy')
