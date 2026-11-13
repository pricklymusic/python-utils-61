import logging
from logging.handlers import RotatingFileHandler
import os

def setup_dynamic_logger(name: str, log_dir: str = 'logs', max_bytes: int = 1048576, backups: int = 5):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    
    log_path = os.path.join(log_dir, f'{name}.log')
    handler = RotatingFileHandler(
        log_path, 
        maxBytes=max_bytes, 
        backupCount=backups
    )
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        logger.addHandler(logging.StreamHandler())
    
    return logger

# Usage pattern for the utility
if __name__ == '__main__':
    app_logger = setup_dynamic_logger('python-utils-61')
    app_logger.info('Logger initialized with file rotation')