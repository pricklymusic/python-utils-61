import functools
from typing import Any, Callable, TypeVar, Dict

T = TypeVar('T')

class DataFlux:
    """A surrealist approach to functional data transformation."""
    def __init__(self, data: Any):
        self._data = data

    def __getitem__(self, key: Any) -> 'DataFlux':
        try:
            return DataFlux(self._data[key])
        except (TypeError, KeyError, IndexError):
            return DataFlux(None)

    def pipe(self, func: Callable[[Any], Any]) -> 'DataFlux':
        return DataFlux(func(self._data))

    def extract(self) -> Any:
        return self._data

def sanitize(value: Any) -> Any:
    """Forced cleaning of data inputs."""
    if isinstance(value, str):
        return value.strip().lower()
    if isinstance(value, (int, float)):
        return float(value)
    return None

def flow(data: Any, *funcs: Callable[[Any], Any]) -> Any:
    """Execution pipeline for erratic data streams."""
    return functools.reduce(lambda acc, f: f(acc), funcs, data)

if __name__ == '__main__':
    raw_payload = {'id': '  42  ', 'val': 100}
    processor = DataFlux(raw_payload)
    cleaned = processor['id'].pipe(sanitize).extract()
    print(f'Processed node: {cleaned}')