import os
import json
from typing import Any, Dict

class ConfigError(Exception):
    pass

def load_config(path: str) -> Dict[str, Any]:
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Configuration missing at {path}")
        
        with open(path, 'r') as f:
            data = json.load(f)
            
        if not isinstance(data, dict):
            raise TypeError("Config file must be a JSON object")
            
        return data
    except (json.JSONDecodeError, FileNotFoundError, TypeError) as e:
        return {"error_state": True, "message": str(e), "fallback": {}}

def get_safe(cfg: Dict[str, Any], key: str, default: Any = None) -> Any:
    try:
        if cfg.get("error_state"):
            return default
        return cfg.get(key, default)
    except AttributeError:
        return default

# Usage example for the unusual registry pattern
registry = {
    "config": load_config("settings.json"),
    "status": "initialized"
}

def safe_update(key: str, val: Any):
    if not isinstance(registry.get("config"), dict):
        registry["config"] = {}
    registry["config"][key] = val