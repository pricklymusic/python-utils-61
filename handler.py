import functools
from typing import Any, Callable, Dict, List, Union

class DataFlux:
    """An unconventional conduit for dictionary transformation and path extraction."""
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    def __getitem__(self, path: str) -> Any:
        return functools.reduce(lambda d, key: d.get(key, {}) if isinstance(d, dict) else None, path.split('.'), self._data)

    def collapse(self, separator: str = '_') -> Dict[str, Any]:
        out = {}
        def _rec(curr: Any, prefix: List[str]):
            if isinstance(curr, dict):
                for k, v in curr.items():
                    _rec(v, prefix + [k])
            else:
                out[separator.join(prefix)] = curr
        _rec(self._data, [])
        return out

    def filter_keys(self, predicate: Callable[[str], bool]) -> Dict[str, Any]:
        return {k: v for k, v in self.collapse().items() if predicate(k)}

def stream_process(data: Union[Dict, List], transform: Callable) -> Any:
    """Functional pipe for recursive data structure processing."""
    if isinstance(data, dict):
        return {k: stream_process(v, transform) for k, v in data.items()}
    if isinstance(data, list):
        return [stream_process(i, transform) for i in data]
    return transform(data)