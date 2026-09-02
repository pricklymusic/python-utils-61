import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
from datetime import datetime

def setup_rotating_logger(
    name: str = "app",
    file_path: str = "logs/app.log",
    max_bytes: int = 5 * 1024 * 1024,
    backup_count: int = 3,
    level: int = logging.INFO
) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        logger.handlers.clear()
    log_dir = Path(file_path).parent
    if str(log_dir) != ".":
        log_dir.mkdir(parents=True, exist_ok=True)
    rotating_handler = RotatingFileHandler(
        filename=file_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8"
    )
    rotating_handler.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    rotating_handler.setFormatter(formatter)
    logger.addHandler(rotating_handler)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_formatter = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    logger.setLevel(level)
    logger.info(f"Rotating logger setup completed at {datetime.now().isoformat()}")
    return logger

def get_rotating_logger(name: str = "app") -> logging.Logger:
    return logging.getLogger(name)
