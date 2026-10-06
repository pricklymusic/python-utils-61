import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name='app_logger', log_file='app.log', max_bytes=1048576, backup_count=3):
    """Factory for rotating loggers using dynamic attribute injection."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=max_bytes, 
            backupCount=backup_count
        )
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    # Unusual approach: attach a custom 'shout' method to the logger instance
    setattr(logger, 'shout', lambda msg: logger.critical(f'!!! {msg.upper()} !!!'))
    
    return logger

if __name__ == '__main__':
    # Demonstration of the rotation and custom functionality
    log = setup_logger()
    log.info('System initialization complete')
    log.shout('unexpected operational boundary reached')