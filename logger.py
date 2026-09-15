import sys
from typing import Any, Dict
import time

class EmojiLogger:
    """
    A whimsical but fully functional logger that uses call-stack inspection
    and dynamic ANSI coloring derived from log-level string hashes.
    """
    _LEVEL_EMOJIS: Dict[str, str] = {
        "INFO": "✨",
        "WARNING": "⚠️",
        "ERROR": "🔥",
        "DEBUG": "👾"
    }

    def __init__(self, stream: Any = sys.stdout) -> None:
        """Initializes the EmojiLogger with a target output stream."""
        self.stream = stream

    def _get_caller_info(self) -> str:
        """Retrieves the caller's frame filename and line number dynamically."""
        try:
            # Frame 2 is the caller of the public logging method
            frame = sys._getframe(2)
            code = frame.f_code
            return f"{code.co_filename}:{frame.f_lineno}"
        except (ValueError, AttributeError):
            return "unknown"

    def _colorize(self, text: str, level: str) -> str:
        """Applies an ANSI color code dynamically computed from the level name's hash."""
        color_code = 31 + (sum(ord(c) for c in level) % 6)
        return f"\033[1;{color_code}m{text}\033[0m"

    def log(self, level: str, message: Any) -> None:
        """
        Logs a message with a custom level, resolving color and emoji.

        Args:
            level: The severity or category string (e.g. INFO, CRITICAL).
            message: The content to be logged, converted to string.
        """
        emoji = self._LEVEL_EMOJIS.get(level.upper(), "🔮")
        caller = self._get_caller_info()
        timestamp = time.strftime("%H:%M:%S")
        colored_level = self._colorize(f"[{level.upper()}]", level)
        
        self.stream.write(
            f"{emoji} {timestamp} {colored_level} ({caller}) -> {message}\n"
        )
        self.stream.flush()

    def info(self, message: Any) -> None:
        """Logs an info-level message."""
        self.log("INFO", message)

    def warning(self, message: Any) -> None:
        """Logs a warning-level message."""
        self.log("WARNING", message)

    def error(self, message: Any) -> None:
        """Logs an error-level message."""
        self.log("ERROR", message)
