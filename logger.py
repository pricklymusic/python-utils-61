import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


class DynamicEmojiFormatter(logging.Formatter):
    """Custom formatter that prefixes log messages with contextual level emojis."""
    
    EMOJI_MAP = {
        logging.DEBUG: "🐛",
        logging.INFO: "ℹ️",
        logging.WARNING: "⚠️",
        logging.ERROR: "❌",
        logging.CRITICAL: "🔥",
    }

    def format(self, record: logging.LogRecord) -> str:
        icon = self.EMOJI_MAP.get(record.levelno, "📝")
        original_msg = record.msg
        record.msg = f"{icon} {original_msg}"
        formatted = super().format(record)
        record.msg = original_msg  # restore original message
        return formatted


def setup_rotating_logger(
    name: str = "app_logger",
    log_file: str = "logs/app.log",
    max_bytes: int = 1_048_576,  # 1 MB default rotation trigger
    backup_count: int = 5,
    level: int = logging.INFO,
    console_output: bool = True,
) -> logging.Logger:
    """Configures and returns a logger instance equipped with size-based file rotation."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    fmt = "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
    formatter = DynamicEmojiFormatter(fmt, datefmt="%Y-%m-%d %H:%M:%S")

    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
