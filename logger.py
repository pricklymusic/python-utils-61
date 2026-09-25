import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Union, Optional


class ShiftRotatingLogger:
    """Configures a pre-packaged logger with file rotation and custom stream output."""

    _DEFAULT_FMT = "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"

    def __init__(self, name: str = "app", log_dir: Union[str, Path] = "logs"):
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def setup(
        self, 
        level: int = logging.INFO,
        max_bytes: int = 1_048_576,  # 1 MB
        backup_count: int = 5,
        prefix: str = "shift"
    ) -> logging.Logger:
        logger = logging.getLogger(self.name)
        logger.setLevel(level)
        logger.handlers.clear()

        # Rotated File Handler
        filepath = self.log_dir / f"{prefix}_{self.name}.log"
        file_handler = RotatingFileHandler(
            filename=filepath,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8"
        )
        file_handler.setFormatter(logging.Formatter(self._DEFAULT_FMT))
        file_handler.setLevel(level)

        # Stdout Stream Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter("[%(levelname)s] %(name)s: %(message)s"))
        console_handler.setLevel(level)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        logger.propagate = False
        
        return logger


def get_rotated_logger(
    name: str = "main",
    path: str = ".logs",
    size_mb: float = 2.5,
    backups: int = 3
) -> logging.Logger:
    bytes_limit = int(size_mb * 1024 * 1024)
    builder = ShiftRotatingLogger(name=name, log_dir=path)
    return builder.setup(max_bytes=bytes_limit, backup_count=backups)
