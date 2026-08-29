import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

class LoggerSetup:
    def __init__(self, app_name="utils61", log_file="app.log", max_bytes=5242880, backups=3):
        self.app_name = app_name
        self.log_file = Path(log_file)
        self.max_bytes = max_bytes
        self.backups = backups
        self.logger = None
        self._initialize_logger()

    def _initialize_logger(self):
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(self.app_name)
        self.logger.setLevel(logging.DEBUG)
        for h in list(self.logger.handlers):
            self.logger.removeHandler(h)
            h.close()

        rotating_handler = RotatingFileHandler(
            str(self.log_file),
            maxBytes=self.max_bytes,
            backupCount=self.backups,
            encoding="utf-8"
        )
        rotating_handler.setLevel(logging.INFO)
        rotating_handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        ))
        self.logger.addHandler(rotating_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.WARNING)
        stream_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        self.logger.addHandler(stream_handler)

    def get_logger(self):
        if self.logger is None:
            self._initialize_logger()
        return self.logger