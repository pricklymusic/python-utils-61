import logging
from logging.handlers import RotatingFileHandler

class CustomLogger:
    def __init__(self, name, log_file, max_bytes=10**6, backup_count=3):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_debug(self, message):
        self.logger.debug(message)

if __name__ == '__main__':
    logger = CustomLogger('MyLogger', 'app.log')
    logger.log_info('This is an info message')
    logger.log_error('This is an error message')