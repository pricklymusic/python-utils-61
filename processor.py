import json
from typing import Any, Dict

class ProcessingError(Exception):
    pass

class DataProcessor:
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    def validate_data(self) -> None:
        if not isinstance(self.data, dict):
            raise ProcessingError('Data must be a dictionary')
        if 'value' not in self.data:
            raise ProcessingError('Missing key: value')
        if not isinstance(self.data['value'], (int, float)):
            raise ProcessingError('Value must be a number')

    def process_data(self) -> float:
        self.validate_data()
        value = self.data['value']
        result = value * 2  # Example processing
        return result

    def to_json(self) -> str:
        try:
            result = self.process_data()
            return json.dumps({'result': result})
        except ProcessingError as e:
            return json.dumps({'error': str(e)})

if __name__ == '__main__':
    processor = DataProcessor({'value': 10})
    print(processor.to_json())  # Output: {"result": 20}
    processor_invalid = DataProcessor({'no_value': 10})
    print(processor_invalid.to_json())  # Output: {"error": "Missing key: value"}