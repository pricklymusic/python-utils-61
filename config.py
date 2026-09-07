import os
from typing import Any, Dict, Type, TypeVar, get_type_hints

T = TypeVar("T", bound="TypedEnvConfig")

class TypedEnvConfig:
    """A self-parsing configuration base class.

    This class leverages class-level type annotations to automatically extract,
    cast, and validate configuration values from environment variables or custom overrides.
    """

    def __init__(self, overrides: Dict[str, Any] | None = None) -> None:
        """Initializes the configuration, applying optional dictionary overrides.

        Args:
            overrides: Optional key-value pairs to override environment variables.
        """
        self._overrides: Dict[str, Any] = overrides or {}
        self._loaded_values: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Parses annotated class variables and binds their typed values."""
        hints = get_type_hints(self.__class__)
        for key, expected_type in hints.items():
            if key.startswith("_"):
                continue
            
            raw_val = self._overrides.get(key) or os.getenv(key.upper())
            if raw_val is None:
                if hasattr(self.__class__, key):
                    # Use class-level default if it exists
                    self._loaded_values[key] = getattr(self.__class__, key)
                    continue
                raise ValueError(f"Missing required configuration: {key.upper()}")

            self._loaded_values[key] = self._cast_value(raw_val, expected_type)

    def _cast_value(self, value: Any, target_type: Type[Any]) -> Any:
        """Casts raw configuration values to their annotated types.

        Args:
            value: The raw string or object to cast.
            target_type: The expected class/type target.
            
        Returns:
            The safely casted object matching target_type.
        """
        if isinstance(value, target_type):
            return value
        if target_type is bool:
            return str(value).lower() in ("true", "1", "yes", "t", "y")
        try:
            return target_type(value)
        except (ValueError, TypeError) as err:
            raise TypeError(f"Cannot cast {value!r} to {target_type}") from err

    def __getattr__(self, item: str) -> Any:
        """Retrieves loaded configurations dynamically.

        Args:
            item: Name of the configuration field.
        """
        if item in self._loaded_values:
            return self._loaded_values[item]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")
