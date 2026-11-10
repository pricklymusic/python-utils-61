import os
from typing import Any, Dict, Type, TypeVar

T = TypeVar("T")

class _ConstantMeta(type):
    def __setattr__(cls, name: str, value: Any) -> None:
        if name in cls.__dict__ and not name.startswith("__"):
            raise AttributeError(f"Cannot reassign frozen constant '{name}'")
        super().__setattr__(name, value)

    def __delattr__(cls, name: str) -> None:
        raise AttributeError(f"Cannot delete constant '{name}'")


class BaseConstants(metaclass=_ConstantMeta):
    """Immutable namespace for constants with env override and auto-casting."""

    @classmethod
    def load_env_overrides(cls, prefix: str = "") -> None:
        for attr, current_val in list(cls.__dict__.items()):
            if attr.startswith("_") or callable(current_val):
                continue
            env_key = f"{prefix}_{attr}".strip("_").upper()
            if env_key in os.environ:
                raw_val = os.environ[env_key]
                casted = cls._cast_type(type(current_val), raw_val)
                type.__setattr__(cls, attr, casted)

    @staticmethod
    def _cast_type(target_type: Type[T], value: str) -> Any:
        if target_type is bool:
            return value.lower() in ("1", "true", "yes", "on")
        if target_type in (int, float, str):
            return target_type(value)
        return value

    @classmethod
    def as_dict(cls) -> Dict[str, Any]:
        return {
            k: v for k, v in cls.__dict__.items()
            if not k.startswith("_") and not isinstance(v, (classmethod, staticmethod))
        }


class AppConstants(BaseConstants):
    DEFAULT_TIMEOUT: int = 30
    ENABLE_CACHE: bool = True
    MAX_RETRIES: int = 3
    LOG_LEVEL: str = "INFO"
    BUFFER_SIZE: int = 8192


class ColorPalette(BaseConstants):
    PRIMARY: str = "#1E88E5"
    SECONDARY: str = "#D81B60"
    SUCCESS: str = "#4CAF50"
    WARNING: str = "#FB8C00"
    ERROR: str = "#E53935"
