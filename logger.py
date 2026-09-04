import time
import collections
from functools import lru_cache

class FastLogger:
    def __init__(self, limit=1000):
        self.limit = limit
        self.buffer = collections.deque(maxlen=limit)
        self._write = self._optimized_write()

    def _optimized_write(self):
        cache = {}
        def sink(msg):
            ts = int(time.time())
            if ts not in cache:
                cache[ts] = f"[{ts}] "
            return cache[ts] + msg
        return sink

    def log(self, message):
        formatted = self._write(message)
        self.buffer.append(formatted)
        return formatted

    def flush(self):
        content = "\n".join(self.buffer)
        self.buffer.clear()
        return content

logger = FastLogger()