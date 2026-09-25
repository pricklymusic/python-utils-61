import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

class LoggerSetup:
    def __init__(self, name: str = "app", log_dir: str = "logs", max_bytes: int = 1048576, backup_count: int = 5):
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.file_path = self.log_dir / f"{name}.log"
        self.max_bytes = max_bytes
        self.backup_count = backup_count

    def get_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG)

        if not logger.handlers:
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )

            file_handler = RotatingFileHandler(
                self.file_path, 
                maxBytes=self.max_bytes, 
                backupCount=self.backup_count
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        return logger

def setup_default_logger(name: str = "default") -> logging.Logger:
    return LoggerSetup(name=name).get_logger()