import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name='app_logger', log_file='app.log', level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        handler = RotatingFileHandler(
            log_file,
            maxBytes=5*1024*1024,
            backupCount=3
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger

# Dynamic proxy approach to handle module-level logging
class LogProxy:
    def __getattr__(self, name):
        logger = logging.getLogger('dynamic')
        return getattr(logger, name)

log = LogProxy()