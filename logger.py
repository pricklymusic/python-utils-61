import os
import logging
from logging.handlers import RotatingFileHandler
from typing import Dict, Union


class SelfCleaningRotatingHandler(RotatingFileHandler):
    """Rotating file handler that automatically provisions target directories."""

    def __init__(self, filename: str, maxBytes: int = 1_048_576, backupCount: int = 5, encoding: str = "utf-8"):
        log_dir = os.path.dirname(filename)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        super().__init__(filename, maxBytes=maxBytes, backupCount=backupCount, encoding=encoding)


class DynamicRotator:
    """Fluent logger wrapper provisioning rotation handlers on demand."""

    _registry: Dict[str, logging.Logger] = {}

    def __init__(self, base_name: str = "app", log_dir: str = "logs"):
        self.base_name = base_name
        self.log_dir = log_dir

    def configure(
        self,
        name: str = "main",
        max_bytes: int = 5 * 1024 * 1024,
        backup_count: int = 3,
        level: Union[int, str] = logging.INFO,
    ) -> logging.Logger:
        full_name = f"{self.base_name}.{name}" if name != "main" else self.base_name
        if full_name in self._registry:
            return self._registry[full_name]

        logger = logging.getLogger(full_name)
        logger.setLevel(level)

        filepath = os.path.join(self.log_dir, f"{name}.log")
        handler = SelfCleaningRotatingHandler(filepath, maxBytes=max_bytes, backupCount=backup_count)

        fmt = logging.Formatter(
            "[%(asctime)s] %(levelname)-8s [%(name)s:%(lineno)d] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(fmt)
        logger.addHandler(handler)

        self._registry[full_name] = logger
        return logger

    def __getattr__(self, name: str) -> logging.Logger:
        return self.configure(name=name)


def setup_rotating_logger(log_path: str = "logs/app.log", max_mb: float = 2.0, backups: int = 5) -> logging.Logger:
    folder = os.path.dirname(log_path) or "logs"
    rotator = DynamicRotator(log_dir=folder)
    channel = os.path.splitext(os.path.basename(log_path))[0]
    return rotator.configure(name=channel, max_bytes=int(max_mb * 1024 * 1024), backup_count=backups)
