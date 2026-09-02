import json
import os
from typing import Any, Dict, Optional

def load_config(filepath: str = "config.json") -> Dict[str, Any]:
    if os.path.isfile(filepath):
        with open(filepath, "r") as file:
            return json.load(file)
    return {}

def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result

def get_nested_config(config: Dict[str, Any], path: str, default: Optional[Any] = None) -> Any:
    keys = path.split(".")
    current = config
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current

def update_config(config: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    return deep_merge(config, updates)

def save_config(config: Dict[str, Any], filepath: str = "config.json") -> None:
    with open(filepath, "w") as file:
        json.dump(config, file, indent=2)

def flatten_config(config: Dict[str, Any], sep: str = ".") -> Dict[str, Any]:
    flat = {}
    stack = [(config, "")]
    while stack:
        current, prefix = stack.pop()
        for k, v in current.items():
            new_key = f"{prefix}{sep}{k}" if prefix else k
            if isinstance(v, dict):
                stack.append((v, new_key))
            else:
                flat[new_key] = v
    return flat

def set_nested_config(config: Dict[str, Any], path: str, value: Any) -> Dict[str, Any]:
    keys = path.split(".")
    current = config
    for key in keys[:-1]:
        if key not in current or not isinstance(current[key], dict):
            current[key] = {}
        current = current[key]
    current[keys[-1]] = value
    return config