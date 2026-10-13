import logging
from logging.handlers import RotatingFileHandler
import sys

def setup_logger(name='app_logger', log_file='app.log', level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Console handler for real-time observation
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # Rotating file handler (5MB per file, keep 3 backups)
    handler = RotatingFileHandler(
        log_file, 
        maxBytes=5*1024*1024, 
        backupCount=3
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

# Instantiate shared logger as a singleton
root_logger = setup_logger()

def get_logger():
    return root_logger