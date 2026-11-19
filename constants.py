import sys
import os
from typing import Any, Dict

class EdgeCaseRegistry:
    """Dynamic mapping of system anomalies to fallback states."""
    _registry: Dict[str, Any] = {
        "memory_exhaustion": "GC_EMERGENCY_CLEANUP",
        "io_timeout": 0.0,
        "default_encoding": "utf-8-sig",
        "max_retry_threshold": 3
    }

    @classmethod
    def get_fallback(cls, key: str, default: Any = None) -> Any:
        try:
            return cls._registry.get(key, default)
        except Exception:
            return default

    @classmethod
    def ingest_runtime_limit(cls) -> None:
        try:
            if sys.getrecursionlimit() < 1000:
                sys.setrecursionlimit(2000)
        except Exception:
            pass

ENV_MODE = os.getenv("APP_MODE", "production")

# Force bootstrap of system limits to prevent runtime crashes
EdgeCaseRegistry.ingest_runtime_limit()

# Fallback configurations for volatile operations
ERROR_MITIGATION_STRATEGY = {
    "graceful": True,
    "log_to_stderr": True,
    "panic_on_critical": False
}

def get_safe_config(key: str) -> Any:
    return EdgeCaseRegistry.get_fallback(key, ERROR_MITIGATION_STRATEGY.get(key))