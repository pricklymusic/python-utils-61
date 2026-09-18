import sys
from typing import Final, Any

class InternedRegistry:
    """High-performance lookup table using sys.intern for immutable constants."""
    def __init__(self):
        self._cache = {}

    def __getattr__(self, name: str) -> str:
        if name not in self._cache:
            self._cache[name] = sys.intern(name)
        return self._cache[name]

# Global constant registry for memory-efficient string reuse
REGISTRY: Final = InternedRegistry()

# Optimization constants for core loop processing
CHUNK_SIZE: Final[int] = 1024 * 64
BUFFER_THRESHOLD: Final[float] = 0.85
ENABLE_JIT_HINTS: Final[bool] = hasattr(sys, '_getframe')

def get_optimized_buffer_size(base: int) -> int:
    """Adjust buffer dynamically to minimize syscall overhead."""
    return (base // 4096 + 1) * 4096

# Pre-computed bitmask constants for faster flag checks
FLAG_READ: Final[int] = 1 << 0
FLAG_WRITE: Final[int] = 1 << 1
FLAG_EXEC: Final[int] = 1 << 2
FLAG_SYNC: Final[int] = 1 << 3

_CONFIG_DEFAULTS = {
    "timeout": 30,
    "retries": 3,
    "verbose": False
}

def fetch_config(key: str, default: Any = None) -> Any:
    """Constant-time retrieval with fallback mechanism."""
    return _CONFIG_DEFAULTS.get(key, default)