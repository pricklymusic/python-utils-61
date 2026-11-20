import logging
from logging.handlers import RotatingFileHandler
import sys

def get_rotating_logger(name: str, log_file: str = 'app.log', level: int = logging.INFO) -> logging.Logger:
    """
    A logger that rotates its files based on size.
    Uses a custom formatter to display thread names for visibility.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        formatter = logging.Formatter(
            '[%(asctime)s] [%(threadName)s] %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # File rotation: 5MB per file, keep 3 backups
        file_handler = RotatingFileHandler(
            log_file, maxBytes=5 * 1024 * 1024, backupCount=3
        )
        file_handler.setFormatter(formatter)
        
        # Standard stream handler for console output
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger

# Quick invocation example
if __name__ == '__main__':
    log = get_rotating_logger('python-utils-61')
    log.info('System initialization complete')