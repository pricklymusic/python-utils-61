import logging
from logging.handlers import RotatingFileHandler
import sys

def get_logger(name='app_logger', log_file='app.log', max_bytes=1048576, backup_count=3):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    file_handler.setFormatter(formatter)
    
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
    
    return logger

if __name__ == '__main__':
    log = get_logger('dev_logger', 'runtime.log')
    log.info('logger initialization sequence completed')