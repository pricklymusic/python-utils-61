import functools
from typing import Any, Callable

def validate_payload(schema: dict) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(data: Any, *args, **kwargs):
            if not isinstance(data, dict):
                raise ValueError('payload must be a dictionary')
            for key, expected_type in schema.items():
                if key not in data or not isinstance(data[key], expected_type):
                    raise TypeError(f'invalid or missing field: {key}')
            return func(data, *args, **kwargs)
        return wrapper
    return decorator

SCHEMA = {'id': int, 'task': str, 'priority': int}

@validate_payload(SCHEMA)
def process_event(event: dict) -> str:
    return f"processing task {event['id']}: {event['task']}"

def main_loop(events: list):
    for event in events:
        try:
            result = process_event(event)
            print(result)
        except (ValueError, TypeError) as e:
            print(f"skipping invalid event: {e}")

if __name__ == '__main__':
    data_stream = [{'id': 1, 'task': 'backup', 'priority': 2}, {'id': 'bad', 'task': 'error', 'priority': 1}]
    main_loop(data_stream)