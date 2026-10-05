import os
from typing import Any, Dict, Optional, Union

class ConfigMapper:
    """Dynamic dictionary proxy with recursive type enforcement."""

    def __init__(self, settings: Optional[Dict[str, Any]] = None) -> None:
        self._data: Dict[str, Any] = settings or {}

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve value with an optional fallback mechanism."""
        return self._data.get(key, default)

    def load_env(self, prefix: str = "APP_") -> None:
        """Ingest system environment variables into configuration storage."""
        for key, value in os.environ.items():
            if key.startswith(prefix):
                clean_key = key[len(prefix):].lower()
                self._data[clean_key] = self._cast_type(value)

    def _cast_type(self, value: str) -> Union[int, float, bool, str]:
        """Attempt conversion of string env vars to native types."""
        if value.lower() in ('true', 'yes'): return True
        if value.lower() in ('false', 'no'): return False
        try:
            if '.' in value: return float(value)
            return int(value)
        except ValueError:
            return value

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __repr__(self) -> str:
        return f"ConfigMapper(keys={list(self._data.keys())})"