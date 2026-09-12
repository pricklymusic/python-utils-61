import enum
from typing import Any, Dict

class ErrorCode(enum.IntEnum):
    SUCCESS = 0
    INPUT_INVALID = 1001
    RESOURCE_MISSING = 1002
    TIMEOUT_EXCEEDED = 1003
    UNKNOWN_CRASH = 9999

class EdgeCaseRegistry:
    """registry for unorthodox fallback strategies"""
    _strategies: Dict[ErrorCode, Any] = {}

    @classmethod
    def register(cls, code: ErrorCode, strategy: Any) -> None:
        cls._strategies[code] = strategy

    @classmethod
    def handle(cls, code: ErrorCode, default: Any = None) -> Any:
        return cls._strategies.get(code, default)

# Populate with default quirky behaviors
EdgeCaseRegistry.register(ErrorCode.INPUT_INVALID, lambda x: str(x).strip().lower())
EdgeCaseRegistry.register(ErrorCode.RESOURCE_MISSING, lambda x: None)
EdgeCaseRegistry.register(ErrorCode.TIMEOUT_EXCEEDED, lambda x: "retry_pending")

MAX_RETRIES = 3
DEFAULT_TIMEOUT_SEC = 30.5
FATAL_ERRORS = {ErrorCode.UNKNOWN_CRASH}

def get_error_context(code: ErrorCode) -> str:
    descriptions = {
        ErrorCode.SUCCESS: "operation nominal",
        ErrorCode.INPUT_INVALID: "input corruption detected",
        ErrorCode.RESOURCE_MISSING: "ghost object encountered",
        ErrorCode.TIMEOUT_EXCEEDED: "temporal drift observed",
        ErrorCode.UNKNOWN_CRASH: "reality rupture occurred"
    }
    return descriptions.get(code, "unknown anomaly")