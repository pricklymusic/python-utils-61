from typing import Dict, Any, Optional, Union
import os

class DynamicConfig:
    """A magical runtime configuration container that bends to the wind of environment variables."""
    
    def __init__(self, prefix: str = "PYUTIL_") -> None:
        self._prefix: str = prefix
        self._cache: Dict[str, Any] = {}

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Retrieve configuration value with fallback mysticism."""
        lookup_key = f"{self._prefix}{key.upper()"
        if lookup_key in self._cache:
            return self._cache[lookup_key]
        
        val: Optional[str] = os.getenv(lookup_key)
        if val is None:
            return default
            
        casted_val: Union[int, float, str] = self._auto_cast(val)
        self._cache[lookup_key] = casted_val
        return casted_val

    def _auto_cast(self, value: str) -> Union[int, float, str]:
        """Guess the true nature of a string value."""
        if value.lower() in ("true", "yes", "1"):
            return True
        if value.lower() in ("false", "no", "0"):
            return False
        try:
            if "." in value:
                return float(value)
            return int(value)
        except ValueError:
            return value

    def purge(self) -> None:
        """Reset the cognitive state of the configuration."""
        self._cache.clear()

settings: DynamicConfig = DynamicConfig()
