import sys
from datetime import datetime
from typing import Any

class CreativeLogger:
    """A minimalist logger using non-standard formatting."""
    def __init__(self, prefix: str = "[61]"):
        self.prefix = prefix

    def __call__(self, message: Any, level: str = "INFO") -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        stream = sys.stderr if level == "ERROR" else sys.stdout
        stream.write(f"{self.prefix} {timestamp} | {level:5} | {message}\n")

    @staticmethod
    def error_decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger = CreativeLogger()
                logger(f"CRITICAL: {e}", "ERROR")
                raise e
        return wrapper

logger = CreativeLogger()

if __name__ == "__main__":
    logger("System initialized")
    logger("Invalid operation", "ERROR")