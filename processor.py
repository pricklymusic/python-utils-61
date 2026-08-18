import json
from typing import Any, Dict, List, Union

class DataProcessor:
    def __init__(self, data: Union[Dict[str, Any], List[Any]]) -> None:
        self.data = data

    def filter_data(self, condition: Any) -> Union[Dict[str, Any], List[Any]]:
        if isinstance(self.data, dict):
            return {k: v for k, v in self.data.items() if condition(v)}
        elif isinstance(self.data, list):
            return [item for item in self.data if condition(item)]
        return self.data

    def transform_data(self, transformer: Any) -> Union[Dict[str, Any], List[Any]]:
        if isinstance(self.data, dict):
            return {k: transformer(v) for k, v in self.data.items()}
        elif isinstance(self.data, list):
            return [transformer(item) for item in self.data]
        return self.data

    def to_json(self) -> str:
        return json.dumps(self.data)

# Example usage:
# processor = DataProcessor({'a': 1, 'b': 2})
# filtered = processor.filter_data(lambda x: x > 1)
# transformed = processor.transform_data(lambda x: x * 2)
# json_output = processor.to_json()
