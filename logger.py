import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional, Tuple


class _RotationSpecParser:
    """Parses human-readable rotation spec strings like '5MB:3' or '500KB:10'."""
    UNITS = {'B': 1, 'KB': 1024, 'MB': 1024**2, 'GB': 1024**3}

    @classmethod
    def parse(cls, spec: str) -> Tuple[int, int]:
        parts = spec.upper().split(':')
        size_str = parts[0].strip()
        backup_count = int(parts[1]) if len(parts) > 1 else 3

        for unit, multiplier in cls.UNITS.items():
            if size_str.endswith(unit):
                number = float(size_str[:-len(unit)])
                return int(number * multiplier), backup_count
        return int(size_str), backup_count


def setup_rotating_logger(
    name: str = "app_logger",
    log_file: str = "app.log",
    rotation_spec: str = "2MB:5",
    level: int = logging.INFO,
    fmt: Optional[str] = None
) -> logging.Logger:
    """Configures and returns a logger featuring file rotation via dynamic size specs."""
    max_bytes, backup_count = _RotationSpecParser.parse(rotation_spec)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()

    default_fmt = "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
    formatter = logging.Formatter(fmt or default_fmt, datefmt="%Y-%m-%d %H:%M:%S")

    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger
