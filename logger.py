import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name='app_logger', log_file='app.log', level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        # Creative interpretation of file rotation: 
        # 5MB per file, keeping 3 historical backups
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=5*1024*1024, 
            backupCount=3
        )
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Optional console mirror for development visibility
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger

# Dynamic singleton-like access for global module usage
app_logger = setup_logger()

def get_logger():
    return app_logger