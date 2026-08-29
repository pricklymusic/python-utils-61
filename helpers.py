import time
from functools import reduce, wraps
from typing import Any, Callable, Dict, List, Optional

def retry(max_attempts: int = 3, delay: float = 1.0) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

def flatten(nested_list: List[Any]) -> List[Any]:
    result: List[Any] = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

def deep_merge(d1: Dict[str, Any], d2: Dict[str, Any]) -> Dict[str, Any]:
    merged = d1.copy()
    for k, v in d2.items():
        if k in merged and isinstance(merged[k], dict) and isinstance(v, dict):
            merged[k] = deep_merge(merged[k], v)
        else:
            merged[k] = v
    return merged

def deep_get(data: Any, path: str, default: Any = None) -> Any:
    if not path:
        return data
    try:
        return reduce(lambda c, k: c[k], path.split('.'), data)
    except (KeyError, TypeError, IndexError, AttributeError):
        return default

def chunk(items: List[Any], size: int) -> List[List[Any]]:
    if size <= 0:
        return []
    return [items[i:i + size] for i in range(0, len(items), size)]

def deduplicate(items: List[Any]) -> List[Any]:
    seen: set = set()
    return [x for x in items if not (x in seen or seen.add(x))]

def safe_divide(a: float, b: float) -> Optional[float]:
    return a / b if b != 0 else None

def batch_processor(func: Callable, data: List[Any], batch_size: int = 10) -> List[Any]:
    results: List[Any] = []
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        batch_results = func(batch) if callable(func) else [func(item) for item in batch]
        results.extend(batch_results if isinstance(batch_results, list) else [batch_results])
    return results
