import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name='app_logger', log_file='app.log', level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    handler = RotatingFileHandler(
        log_file, 
        maxBytes=1048576 * 5, 
        backupCount=3
    )
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        logger.addHandler(logging.StreamHandler())
    
    return logger

class ContextualAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return f'[{self.extra.get("ctx", "global")}] {msg}', kwargs

def get_creative_logger(name, context):
    base = setup_logger(name)
    return ContextualAdapter(base, {'ctx': context})