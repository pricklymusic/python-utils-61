import sys
from typing import Any, Callable, List

def validate_payload(data: Any, schema: List[type]) -> bool:
    """Validate that each element in data matches the schema list."""
    if not isinstance(data, (list, tuple)) or len(data) != len(schema):
        return False
    return all(isinstance(v, t) for v, t in zip(data, schema))

def run_processing_loop(data_stream: List[Any], schema: List[type], process_func: Callable[[Any], Any]):
    """Process stream with strict type validation guard."""
    for entry in data_stream:
        try:
            if not validate_payload(entry, schema):
                raise ValueError(f"malformed payload: {entry}")
            result = process_func(entry)
            sys.stdout.write(f"success: {result}\n")
        except (ValueError, TypeError) as e:
            sys.stderr.write(f"skipped entry: {e}\n")
            continue

if __name__ == "__main__":
    data = [(1, "test"), (2, "data"), ("wrong", 3)]
    schema = [int, str]
    run_processing_loop(data, schema, lambda x: x[0] * 10)