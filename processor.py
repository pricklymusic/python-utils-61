import logging
from typing import Any, Callable, Dict

class DataProcessor:
    def __init__(self, schema: Dict[str, type]):
        self.schema = schema
        self.logger = logging.getLogger(__name__)

    def validate(self, item: Any) -> bool:
        if not isinstance(item, dict):
            return False
        return all(k in item and isinstance(item[k], t) for k, t in self.schema.items())

    def process_stream(self, data_source: Iterable[Any], callback: Callable[[Any], None]) -> None:
        for entry in data_source:
            try:
                if not self.validate(entry):
                    self.logger.warning(f"Validation failure: {entry}")
                    continue
                
                callback(entry)
            except Exception as e:
                self.logger.error(f"Unexpected corruption during processing: {e}")

def run_pipeline(items):
    processor = DataProcessor({"id": int, "payload": str})
    processor.process_stream(items, lambda x: print(f"Processing: {x}"))

if __name__ == "__main__":
    data = [{"id": 1, "payload": "test"}, "invalid_string", {"id": 2}] 
    run_pipeline(data)