import os
import logging
from logging.handlers import RotatingFileHandler
import gzip
import shutil

class GzipRotatingFileHandler(RotatingFileHandler):
    def doRollover(self):
        super().doRollover()
        old_log = self.baseFilename + ".1"
        if os.path.exists(old_log):
            compressed_log = f"{old_log}.gz"
            try:
                with open(old_log, "rb") as f_in:
                    with gzip.open(compressed_log, "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.remove(old_log)
            except Exception:
                pass

def setup_logger(name: str, log_file: str = "app.log") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler = GzipRotatingFileHandler(log_file, maxBytes=1024, backupCount=3, encoding="utf-8")
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger

if __name__ == "__main__":
    log = setup_logger("processor")
    for i in range(100):
        log.info(f"Processing tracking entry index: {i}")