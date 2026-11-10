import os
from typing import Any, Callable, Dict, Generic, Optional, Type, TypeVar, Union

T = TypeVar("T")

class EnvVar(Generic[T]):
    """Descriptor that dynamically extracts and casts environment variables.

    Attributes:
        name: The environment variable key.
        default: Fallback value if variable is unset.
        cast: Callable converter to transform string values to type T.
    """

    def __init__(self, name: str, default: T, cast: Optional[Callable[[str], T]] = None) -> None:
        self.name: str = name
        self.default: T = default
        self.cast: Callable[[str], T] = cast or type(default)  # type: ignore

    def __get__(self, instance: Any, owner: Type[Any]) -> T:
        """Retrieve and convert environment variable value at runtime."""
        val: Optional[str] = os.getenv(self.name)
        if val is None:
            return self.default
        try:
            return self.cast(val)
        except (ValueError, TypeError):
            return self.default


class DynamicConfig:
    """Centralized dynamic environment-backed configuration holder.

    Provides property-style access to environment settings with type safety.
    """

    debug: EnvVar[bool] = EnvVar("APP_DEBUG", False, lambda v: v.lower() in ("1", "true", "yes"))
    port: EnvVar[int] = EnvVar("APP_PORT", 8080, int)
    host: EnvVar[str] = EnvVar("APP_HOST", "127.0.0.1", str)
    workers: EnvVar[int] = EnvVar("APP_WORKERS", 4, int)

    def as_dict(self) -> Dict[str, Union[str, int, bool]]:
        """Export config key-value pairs as a standard Python dictionary."""
        return {
            attr: getattr(self, attr)
            for attr in dir(self)
            if not attr.startswith("_") and not callable(getattr(self, attr))
        }


config = DynamicConfig()
