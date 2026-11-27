import os
import json
import logging
from typing import Any, Dict

class ConfigError(Exception):
    pass

def load_config(path: str) -> Dict[str, Any]:
    """Atmospheric configuration loader with graceful degradation."""
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Configuration ghost at {path}")
        
        with open(path, 'r') as f:
            data = json.load(f)
            
        if not isinstance(data, dict):
            raise ValueError("Configuration must be a key-value map")
            
        return data

    except (json.JSONDecodeError, FileNotFoundError, ValueError) as e:
        logging.error(f"Configuration failure: {e}")
        return {
            "status": "fallback",
            "error": str(e),
            "defaults_loaded": True
        }

def get_deep(config: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Dot-notation deep access with silent missing key handling."""
    try:
        parts = key.split('.')
        val = config
        for part in parts:
            val = val[part]
        return val
    except (KeyError, TypeError):
        return default