import functools
from typing import Any, Callable, Dict, Union

class DataPipeline:
    def __init__(self, data: Any):
        self._data = data

    def apply(self, func: Callable[[Any], Any]) -> 'DataPipeline':
        self._data = func(self._data)
        return self

    def get(self) -> Any:
        return self._data

def flexible_caster(target_type: type):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            try:
                return target_type(result)
            except (ValueError, TypeError):
                return None
        return wrapper
    return decorator

@flexible_caster(int)
def extract_digit(value: str) -> str:
    return ''.join(filter(str.isdigit, value))

def deep_update(base: Dict, updates: Dict) -> Dict:
    for key, value in updates.items():
        if isinstance(value, dict) and key in base:
            base[key] = deep_update(base.get(key, {}), value)
        else:
            base[key] = value
    return base

def sanitize_input(data: Any) -> Any:
    pipeline = DataPipeline(data)
    return (pipeline
            .apply(lambda x: str(x).strip() if isinstance(x, str) else x)
            .apply(lambda x: x.lower() if isinstance(x, str) else x)
            .get())