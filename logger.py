import logging
import logging.handlers
import os

log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

class CustomLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.handlers.RotatingFileHandler(
            os.path.join(log_directory, 'app.log'),
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=3
        )
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger

# Usage example:
# custom_logger = CustomLogger(__name__).get_logger()
# custom_logger.info('This is an info message.')