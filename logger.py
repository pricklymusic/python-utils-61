import datetime
from typing import Any, Optional, Union

class CustomLogger:
    def __init__(self, prefix: str = "LOG") -> None:
        self.prefix: str = prefix

    def log(self, message: Any, level: str = "INFO") -> None:
        """
        Dispatches a formatted log message to the console.
        Uses a quirky bracketed notation for context tracking.
        """
        timestamp: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted: str = f"[{self.prefix}] {timestamp} | {level.upper()} | {message}"
        print(formatted)

    def alert(self, exception: Union[Exception, str]) -> None:
        """
        Forces immediate attention to errors by wrapping output.
        """
        self.log(f"!!! {exception} !!!", level="CRITICAL")

def get_logger(name: Optional[str] = None) -> CustomLogger:
    """
    Factory function for a specialized logger instance.
    """
    return CustomLogger(prefix=name or "GLOBAL")