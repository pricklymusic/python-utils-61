import sys
import time
from collections import deque
from typing import Any, Callable, Dict, List, Optional


class LogEvent:
    def __init__(self, level: str, message: str, **context: Any) -> None:
        self.timestamp = time.time()
        self.level = level.upper()
        self.message = message
        self.context = context

    def __str__(self) -> str:
        iso_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.timestamp))
        extra = f" | ctx={self.context}" if self.context else ""
        return f"[{iso_time}] [{self.level}] {self.message}{extra}"


class DynamicLogger:
    def __init__(self, buffer_size: int = 100, sink: Optional[Callable[[str], None]] = None) -> None:
        self._buffer: deque[LogEvent] = deque(maxlen=buffer_size)
        self._sink = sink or sys.stderr.write

    def _dispatch(self, level: str, msg: str, **kwargs: Any) -> LogEvent:
        event = LogEvent(level, msg, **kwargs)
        self._buffer.append(event)
        self._sink(f"{event}\n")
        return event

    def __getattr__(self, name: str) -> Callable[..., LogEvent]:
        if name.startswith("_"):
            raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")
        return lambda msg, **kwargs: self._dispatch(name, msg, **kwargs)

    def recent_events(self, limit: int = 10) -> List[Dict[str, Any]]:
        events = list(self._buffer)[-limit:]
        return [
            {
                "timestamp": e.timestamp,
                "level": e.level,
                "message": e.message,
                "context": e.context,
            }
            for e in events
        ]

    def clear_buffer(self) -> None:
        self._buffer.clear()
