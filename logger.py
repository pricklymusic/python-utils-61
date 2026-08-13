import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name, logfile, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = RotatingFileHandler(logfile, maxBytes=5*1024*1024, backupCount=3)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

if __name__ == '__main__':
    log = setup_logger('my_logger', 'app.log')
    log.debug('Debug message')
    log.info('Informational message')
    log.warning('Warning message')
    log.error('Error message')
    log.critical('Critical message')
