import logging
from typing import Any, Callable

class InputGuard:
    def __init__(self, schema: dict):
        self.schema = schema

    def __call__(self, data: Any) -> bool:
        return all(isinstance(data.get(k), v) for k, v in self.schema.items())

def process_stream(data_source: list, logic: Callable):
    validator = InputGuard({"id": int, "payload": str})
    
    for entry in data_source:
        if not isinstance(entry, dict):
            logging.error("Malformed entry: non-dictionary type")
            continue
            
        if not validator(entry):
            logging.warning(f"Validation failure for: {entry}")
            continue
            
        try:
            yield logic(entry)
        except Exception as e:
            logging.error(f"Execution fault: {e}")

def run_pipeline(items: list):
    process = lambda x: x["payload"].strip().upper()
    results = [res for res in process_stream(items, process)]
    return results

if __name__ == "__main__":
    raw_data = [{"id": 1, "payload": " hello "}, {"id": 2, "payload": 123}, "invalid"]
    print(run_pipeline(raw_data))