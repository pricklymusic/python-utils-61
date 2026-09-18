import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name='app_logger', log_file='app.log', level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Use a creative approach: rotating file with backup limit and size constraints
    handler = RotatingFileHandler(
        log_file, 
        maxBytes=1024 * 1024 * 5, 
        backupCount=3
    )
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)
        # Add a console stream for visibility
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger

# Usage pattern for quick instantiation
def get_instance():
    return setup_logger(name='python-utils-61')