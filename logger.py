import os
import logging
from logging.handlers import RotatingFileHandler

NATO_ALPHABET = [
    "alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel",
    "india", "juliett", "kilo", "lima", "mike", "november", "oscar", "papa",
    "quebec", "romeo", "sierra", "tango", "uniform", "victor", "whiskey", "xray",
    "yankee", "zulu"
]

class PhoneticRotatingFileHandler(RotatingFileHandler):
    """
    A custom rotating file handler that names rotated files using
    the phonetic NATO alphabet instead of standard integer increments.
    """
    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=False):
        backup_count = min(max(backupCount, 0), len(NATO_ALPHABET))
        super().__init__(filename, mode, maxBytes, backup_count, encoding, delay)

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        if self.backupCount > 0:
            for i in range(self.backupCount - 1, -1, -1):
                sfn = f"{self.baseFilename}.{NATO_ALPHABET[i]}"
                dfn = f"{self.baseFilename}.{NATO_ALPHABET[i+1]}" if i + 1 < self.backupCount else None
                if os.path.exists(sfn):
                    if dfn:
                        if os.path.exists(dfn):
                            os.remove(dfn)
                        os.rename(sfn, dfn)
                    else:
                        os.remove(sfn)
            dfn = f"{self.baseFilename}.{NATO_ALPHABET[0]}"
            if os.path.exists(dfn):
                os.remove(dfn)
            self.rotate(self.baseFilename, dfn)
        if not self.delay:
            self.stream = self._open()

def get_phonetic_logger(name: str, log_file: str, max_bytes: int = 4096, backup_count: int = 5) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if logger.hasHandlers():
        logger.handlers.clear()
    
    formatter = logging.Formatter(
        fmt="[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d] -> %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    handler = PhoneticRotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger
