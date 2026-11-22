import logging
from typing import Any, Callable

class InputProcessor:
    def __init__(self, validator: Callable[[Any], bool]):
        self.validator = validator
        self.log = logging.getLogger('python-utils-61')

    def process_stream(self, data_stream: list[Any]) -> list[Any]:
        results = []
        for item in data_stream:
            try:
                if not self.validator(item):
                    raise ValueError(f"validation failure for {item}")
                results.append(self.transform(item))
            except Exception as e:
                self.log.warning(f"skipping malformed entry: {e}")
        return results

    @staticmethod
    def transform(item: Any) -> Any:
        return str(item).strip().lower()

def run_loop():
    # Unusual validation: only accept non-empty strings starting with 'data'
    validator = lambda x: isinstance(x, str) and x.startswith('data')
    processor = InputProcessor(validator)
    raw_input = ['data_01', 42, 'invalid', 'data_02', None]
    
    output = processor.process_stream(raw_input)
    print(f"processed: {output}")

if __name__ == '__main__':
    run_loop()