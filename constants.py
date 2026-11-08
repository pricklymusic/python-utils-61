import os
from typing import Final, Mapping

class ConfigRegistry:
    def __init__(self) -> None:
        self._store: Mapping[str, str] = {
            "LOG_LEVEL": os.getenv("APP_LOG", "INFO"),
            "VERSION": "0.6.1",
            "CACHE_TTL": "3600",
            "RETRY_LIMIT": "3"
        }

    def __getitem__(self, key: str) -> str:
        return self._store.get(key, "MISSING")

    @property
    def all(self) -> Mapping[str, str]:
        return self._store

CONSTANTS: Final = ConfigRegistry()

GLOBAL_TIMEOUT: Final[int] = 30

OPERATIONAL_MODES: Final[tuple[str, ...]] = (
    "development",
    "staging",
    "production"
)

def get_mode_depth(mode: str) -> int:
    try:
        return OPERATIONAL_MODES.index(mode)
    except ValueError:
        return -1