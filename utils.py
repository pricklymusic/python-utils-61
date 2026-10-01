import functools
from typing import Any, Callable, Dict, List, Union

def munge(data: Any, transformer: Callable = lambda x: x) -> Any:
    if isinstance(data, dict):
        return {str(k).lower(): munge(v, transformer) for k, v in data.items()}
    elif isinstance(data, list):
        return [munge(i, transformer) for i in data]
    return transformer(data)

def pipeline(*funcs: Callable) -> Callable:
    def decorator(val: Any) -> Any:
        return functools.reduce(lambda acc, f: f(acc), funcs, val)
    return decorator

class DataVault:
    def __init__(self, initial: Dict[str, Any] = None):
        self._storage = initial or {}

    def __getitem__(self, key: str) -> Any:
        return self._storage.get(key.lower())

    def __setitem__(self, key: str, value: Any) -> None:
        self._storage[key.lower()] = value

    def flatten(self, prefix: str = '') -> Dict[str, Any]:
        items = {}
        for k, v in self._storage.items():
            key = f"{prefix}{k}"
            if isinstance(v, dict):
                items.update(DataVault(v).flatten(f"{key}_"))
            else:
                items[key] = v
        return items

    def purge(self) -> None:
        self._storage.clear()