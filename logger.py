import logging
from logging.handlers import RotatingFileHandler
import os

class LoggerManager:
    def __init__(self, log_file='app.log', max_size=1024*1024, backups=3):
        self.log_file = log_file
        self.max_size = max_size
        self.backups = backups
        self.logger = logging.getLogger('python-utils-61')
        self.logger.setLevel(logging.DEBUG)
        self._setup()

    def _setup(self):
        if self.logger.hasHandlers():
            return
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        handler = RotatingFileHandler(
            self.log_file, 
            maxBytes=self.max_size, 
            backupCount=self.backups
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        self.logger.addHandler(console)

    def get_logger(self):
        return self.logger

def setup_global_logger():
    manager = LoggerManager()
    return manager.get_logger()