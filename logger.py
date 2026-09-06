import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

class LoggerSystem:
    def __init__(self, name: str, log_dir: str = 'logs'):
        self.path = Path(log_dir)
        self.path.mkdir(exist_ok=True)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self._setup_handlers()

    def _setup_handlers(self):
        file_path = self.path / 'application.log'
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s'
        )

        console = logging.StreamHandler()
        console.setFormatter(formatter)
        
        rotator = RotatingFileHandler(
            file_path, 
            maxBytes=1_048_576, 
            backupCount=5
        )
        rotator.setFormatter(formatter)

        self.logger.addHandler(console)
        self.logger.addHandler(rotator)

    def get(self):
        return self.logger

def get_logger(name: str):
    return LoggerSystem(name).get()