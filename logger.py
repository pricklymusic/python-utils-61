import logging
from logging.handlers import RotatingFileHandler
import sys
from pathlib import Path

class LoggerOrchestrator:
    def __init__(self, name='app_logger', log_dir='logs', max_bytes=1048576, backups=5):
        self.log_path = Path(log_dir)
        self.log_path.mkdir(exist_ok=True)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        fmt = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s')
        
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(fmt)
        self.logger.addHandler(sh)
        
        fh = RotatingFileHandler(
            self.log_path / f'{name}.log', 
            maxBytes=max_bytes, 
            backupCount=backups
        )
        fh.setFormatter(fmt)
        self.logger.addHandler(fh)

    def get(self):
        return self.logger

def setup_logger(name='main', path='logs'):
    return LoggerOrchestrator(name, path).get()