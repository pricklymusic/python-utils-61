from typing import Dict, Any

class Config:
    def __init__(self, config_data: Dict[str, Any]) -> None:
        self._config_data = config_data

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve the value for the specified key.
        If the key does not exist, return the default value.
        """
        return self._config_data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set the value for a specified key.
        If the key already exists, it will be updated.
        """
        self._config_data[key] = value

    def remove(self, key: str) -> None:
        """
        Remove the specified key from the configuration.
        If the key does not exist, do nothing.
        """
        self._config_data.pop(key, None)

    def keys(self) -> list[str]:
        """
        Return a list of all keys in the configuration.
        """
        return list(self._config_data.keys())

    def values(self) -> list[Any]:
        """
        Return a list of all values in the configuration.
        """
        return list(self._config_data.values())

    def items(self) -> list[tuple[str, Any]]:
        """
        Return a list of all key-value pairs in the configuration.
        """
        return list(self._config_data.items())
