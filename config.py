import json
from pathlib import Path
from typing import Any, Dict, Optional

class ConfigLoader:
    def __init__(self, defaults: Optional[Dict[str, Any]] = None, filepath: Optional[str] = None) -> None:
        self.defaults: Dict[str, Any] = defaults or {}
        self.data: Dict[str, Any] = {}
        if filepath:
            self.load(filepath)
        self._apply_defaults()

    def load(self, filepath: str) -> None:
        path = Path(filepath)
        if path.is_file():
            with open(path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def _apply_defaults(self) -> None:
        def merge(target: Dict[str, Any], source: Dict[str, Any]) -> Dict[str, Any]:
            for k, v in source.items():
                if k not in target:
                    target[k] = v
                elif isinstance(target[k], dict) and isinstance(v, dict):
                    target[k] = merge(target[k], v)
            return target
        self.data = merge(self.data, self.defaults)

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split(".")
        current = self.data
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return default
        return current

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError
        if name in self.data:
            val = self.data[name]
            if isinstance(val, dict):
                return ConfigLoader(defaults=val)
            return val
        raise AttributeError(f"No attribute {name}")

    def set(self, key: str, value: Any) -> None:
        keys = key.split(".")
        current = self.data
        for k in keys[:-1]:
            if k not in current or not isinstance(current[k], dict):
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value

    def save(self, filepath: str) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

    def __repr__(self) -> str:
        return f"<ConfigLoader {self.data}>"

if __name__ == "__main__":
    defaults = {"server": {"host": "127.0.0.1", "port": 8080}, "debug": False}
    config = ConfigLoader(defaults=defaults)
    print(config.server.host)
    print(config.get("debug"))
    config.set("server.port", 9000)
    print(config.get("server.port"))