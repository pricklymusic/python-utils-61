import gzip
import logging
import os
import shutil
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional, Union


class GZRotatingFileHandler(RotatingFileHandler):
    """Rotating file handler that automatically compresses old logs into gzip archives."""

    def doRollover(self) -> None:
        if self.stream:
            self.stream.close()
            self.stream = None

        super().doRollover()

        for i in range(1, self.backupCount + 1):
            sfn = f"{self.baseFilename}.{i}"
            gz_sfn = f"{sfn}.gz"
            if os.path.exists(sfn) and not os.path.exists(gz_sfn):
                with open(sfn, "rb") as f_in:
                    with gzip.open(gz_sfn, "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.remove(sfn)


def setup_logger(
    name: str = "app",
    log_dir: Union[str, Path] = "logs",
    max_bytes: int = 1024 * 1024,
    backup_count: int = 5,
    level: int = logging.INFO,
    fmt: Optional[str] = None,
) -> logging.Logger:
    target_dir = Path(log_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()

    pattern = fmt or "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    formatter = logging.Formatter(pattern, datefmt="%Y-%m-%d %H:%M:%S")

    log_file = target_dir / f"{name}.log"
    file_handler = GZRotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
