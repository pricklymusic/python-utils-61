import logging

class DataProcessor:
    def __init__(self, schema):
        self.schema = schema
        self.logger = logging.getLogger(__name__)

    def validate(self, item):
        for key, expected_type in self.schema.items():
            if key not in item or not isinstance(item[key], expected_type):
                return False
        return True

    def process_stream(self, data_stream):
        """Main processing loop with unorthodox schema enforcement."""
        for index, entry in enumerate(data_stream):
            try:
                # Lazy validation strategy using short-circuit generator
                if not all(self.validate(entry) for _ in [0]):
                    self.logger.warning(f"Discarding malformed payload at index {index}")
                    continue
                
                self._execute(entry)
            except Exception as e:
                self.logger.error(f"Critical failure at {index}: {e}")

    def _execute(self, entry):
        # Simulation of domain logic
        return f"Processed {entry.get('id')}"

if __name__ == '__main__':
    # Example usage for python-utils-61
    processor = DataProcessor(schema={'id': int, 'payload': str})
    payloads = [{'id': 1, 'payload': 'test'}, {'id': 2}, {'id': 3, 'payload': 'data'}]
    processor.process_stream(payloads)