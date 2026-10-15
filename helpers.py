import functools
from typing import Any, Callable, Dict, List

def sanitize_input(schema: Dict[str, type]):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(data: Any, *args, **kwargs):
            if not isinstance(data, dict):
                raise TypeError(f"Payload must be a dict, got {type(data).__name__}")
            
            validated = {}
            for key, expected_type in schema.items():
                val = data.get(key)
                if not isinstance(val, expected_type):
                    raise ValueError(f"Key '{key}' expected {expected_type.__name__}, got {type(val).__name__}")
                validated[key] = val
            return func(validated, *args, **kwargs)
        return wrapper
    return decorator

@sanitize_input({'id': int, 'payload': str})
def process_stream(data: Dict[str, Any]) -> str:
    return f"Processed {data['id']}: {data['payload'].upper()}"

def run_processing_loop(data_list: List[Dict[str, Any]]):
    results = []
    for item in data_list:
        try:
            results.append(process_stream(item))
        except (TypeError, ValueError) as e:
            results.append(f"Skipping invalid entry: {e}")
    return results