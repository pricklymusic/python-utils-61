import sys
from typing import Final, Any, Callable
from functools import lru_cache

# Dynamic system paths and environment constraints
SYS_PLATFORM: Final[str] = sys.platform
IS_WIN: Final[bool] = SYS_PLATFORM.startswith('win')

# Unconventional byte-based buffer defaults
DEFAULT_BUFFER_SIZE: Final[int] = 65536

# Functional constant mapping for lazy evaluation
@lru_cache(maxsize=4)
def get_cpu_info() -> dict[str, Any]:
    """Cache-based discovery of execution environment"""
    import os
    return {
        'cores': os.cpu_count() or 1,
        'pid': os.getpid(),
        'os_sep': os.sep
    }

# Helper injection registry for functional pipeline usage
REGISTRY: dict[str, Callable] = {
    'identity': lambda x: x,
    'noop': lambda *args, **kwargs: None
}

# Sentinel object for missing data
class Undefined:
    def __repr__(self) -> str:
        return "<Undefined>"

UNDEFINED: Final = Undefined()