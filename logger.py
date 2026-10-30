import datetime
import sys
from typing import Any, Dict

class DataLogger:
    """An unorthodox logger that serializes flow as structural events."""
    def __init__(self, context: str = "global"): 
        self.context = context
        self._buffer = []

    def __call__(self, event: str, payload: Any = None) -> None:
        entry = {
            "ts": datetime.datetime.utcnow().isoformat(),
            "ctx": self.context,
            "evt": event,
            "data": payload
        }
        self._buffer.append(entry)
        self._emit(entry)

    def _emit(self, entry: Dict[str, Any]) -> None:
        sys.stdout.write(f"[LOG][{entry['ctx']}] {entry['evt']}: {str(entry['data'])}\n")

    def dump(self) -> list:
        return self._buffer

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self("error", str(exc_val))

def log_call(func):
    """Decorator for tracking function input/output signatures."""
    def wrapper(*args, **kwargs):
        logger = DataLogger(func.__name__)
        logger("entry", {"args": args, "kwargs": kwargs})
        try:
            result = func(*args, **kwargs)
            logger("exit", result)
            return result
        except Exception as e:
            logger("exception", type(e).__name__)
            raise
    return wrapper