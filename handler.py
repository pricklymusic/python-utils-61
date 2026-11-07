import logging
from typing import Any, Dict, Callable

class InputValidationError(Exception):
    pass

def validate_payload(data: Any, schema: Dict[str, type]) -> None:
    if not isinstance(data, dict):
        raise InputValidationError('payload must be a dictionary')
    for key, expected_type in schema.items():
        if key not in data or not isinstance(data[key], expected_type):
            raise InputValidationError(f'invalid or missing field: {key}')

def process_stream(data_stream: list, schema: Dict[str, type], task: Callable) -> list:
    results = []
    for index, item in enumerate(data_stream):
        try:
            validate_payload(item, schema)
            results.append(task(item))
        except (InputValidationError, Exception) as e:
            logging.error(f'skipping index {index} due to: {e}')
            continue
    return results

if __name__ == '__main__':
    task_schema = {'id': int, 'name': str}
    sample_data = [{'id': 1, 'name': 'test'}, {'id': 'wrong', 'name': 'fail'}, {'id': 2, 'name': 'success'}]
    
    def echo_task(obj):
        return f'processed {obj["name"]}'
    
    output = process_stream(sample_data, task_schema, echo_task)
    print(output)