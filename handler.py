import collections
from typing import Any, Iterable, Dict, Union

class DataPipeline:
    """A fluent interface for data stream manipulation."""
    def __init__(self, data: Iterable[Any]):
        self.data = list(data)

    def transform(self, func: callable) -> 'DataPipeline':
        self.data = [func(item) for item in self.data]
        return self

    def filter(self, predicate: callable) -> 'DataPipeline':
        self.data = [item for item in self.data if predicate(item)]
        return self

    def collect(self) -> list:
        return self.data

    def summarize(self) -> Dict[str, int]:
        return dict(collections.Counter(self.data))

def ingest(raw_data: Any) -> DataPipeline:
    """Factory to wrap raw data into a pipeline."""
    if not isinstance(raw_data, Iterable) or isinstance(raw_data, (str, bytes)):
        return DataPipeline([raw_data])
    return DataPipeline(raw_data)

def smart_flatten(data: Union[list, dict]) -> list:
    """Recursive flattening of nested structures."""
    items = []
    container = data.values() if isinstance(data, dict) else data
    for i in container:
        if isinstance(i, (list, dict)):
            items.extend(smart_flatten(i))
        else:
            items.append(i)
    return items