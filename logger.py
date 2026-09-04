import sys
import datetime
from typing import Any, Optional, TextIO

class CreativeLogger:
    """An unconventional logger that pipes output to specific streams."""

    def __init__(self, prefix: str = "LOG", stream: TextIO = sys.stdout) -> None:
        self.prefix: str = prefix
        self.stream: TextIO = stream

    def emit(self, message: Any, level: str = "INFO") -> None:
        """Formats and dispatches a message to the configured stream."""
        timestamp: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        payload: str = f"[{timestamp}] {self.prefix} | {level.upper()} | {message}"
        print(payload, file=self.stream)

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        """Allows the logger instance to act as a functional printer."""
        self.emit(" ".join(map(str, args)))

def get_logger(name: str, output: Optional[TextIO] = None) -> CreativeLogger:
    """Factory function for creating scoped logger instances."""
    return CreativeLogger(prefix=name, stream=output or sys.stdout)