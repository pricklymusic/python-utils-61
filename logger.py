import datetime
from typing import Any, Optional, Union

class CustomLogger:
    def __init__(self, prefix: str = "LOG") -> None:
        self.prefix: str = prefix

    def log(self, message: Any, level: str = "INFO") -> str:
        """
        Prints a message with a timestamp and a level prefix.
        Returns the formatted string for potential further use.
        """
        timestamp: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted: str = f"[{timestamp}] {self.prefix.upper()} | {level.upper()}: {message}"
        print(formatted)
        return formatted

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        """
        Callable interface for quick logging actions.
        """
        msg: str = " ".join(map(str, args))
        self.log(msg, kwargs.get("level", "INFO"))

def get_logger(name: Optional[str] = None) -> CustomLogger:
    """
    Factory function to retrieve a configured logger instance.
    """
    return CustomLogger(prefix=name or "ROOT")