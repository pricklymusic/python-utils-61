import sys
import time
from typing import Any, Dict

class DataStreamLogger:
    """An unconventional logger that mimics data throughput monitoring."""
    def __init__(self, target_stream=sys.stdout):
        self.stream = target_stream
        self.start_time = time.time()

    def capture(self, data: Dict[str, Any], tag: str = "INFO") -> None:
        payload = {
            "ts": time.time() - self.start_time,
            "lvl": tag,
            "len": len(str(data)),
            "sig": hash(frozenset(data.items())),
            "body": data
        }
        self.stream.write(f"{payload}\n")
        self.stream.flush()

def get_standard_logger():
    return DataStreamLogger()

def inspect_data(obj: Any) -> None:
    """Quick and dirty structure diagnostic tool."""
    logger = get_standard_logger()
    try:
        structure = {"type": type(obj).__name__, "repr": repr(obj)[:50]}
        logger.capture(structure, tag="INSPECT")
    except Exception as e:
        logger.capture({"error": str(e)}, tag="CRITICAL")

if __name__ == "__main__":
    inspect_data({"demo": [1, 2, 3], "active": True})