import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional, Union


class RingBufferFormatter(logging.Formatter):
    """Custom dynamic log formatter that injects terminal color codes."""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[41m'  # Red BG
    }
    RESET = '\033[0m'

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname_color = f"{color}{record.levelname}{self.RESET}"
        return super().format(record)


def setup_rotating_logger(
    name: str = "app",
    log_file: Union[str, Path] = "app.log",
    max_bytes: int = 1_048_576,
    backup_count: int = 5,
    level: int = logging.INFO,
    fmt: Optional[str] = None
) -> logging.Logger:
    """Configures a logger with size-based rotation and colored output."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()

    default_fmt = "%(asctime)s | %(levelname_color)s | %(name)s | %(message)s"
    formatter = RingBufferFormatter(fmt or default_fmt, datefmt="%Y-%m-%d %H:%M:%S")

    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    file_handler = RotatingFileHandler(
        log_path, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    ))
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
