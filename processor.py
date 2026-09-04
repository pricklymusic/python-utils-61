import logging
from typing import Any, Callable, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('processor')

class DataValidator:
    def __init__(self, schema: Dict[str, type]):
        self.schema = schema

    def validate(self, data: Any) -> bool:
        if not isinstance(data, dict):
            return False
        return all(isinstance(data.get(k), v) for k, v in self.schema.items())

def process_stream(data_source: list, transform_func: Callable[[dict], None]) -> None:
    """
    Main processing loop with aggressive input sanitation.
    """
    schema = {'id': int, 'payload': str}
    validator = DataValidator(schema)

    for item in data_source:
        try:
            if not validator.validate(item):
                logger.warning(f"Discarding malformed packet: {item}")
                continue
            
            # Execute transformation with internal sanity checks
            if len(item['payload']) > 1024:
                raise ValueError("Payload exceeds max buffer limit")
                
            transform_func(item)
            
        except Exception as e:
            logger.error(f"Critical loop failure: {str(e)}")
            continue

if __name__ == '__main__':
    mock_data = [{'id': 1, 'payload': 'init'}, {'id': 'fail', 'payload': 123}, {'id': 2, 'payload': 'data'}]
    process_stream(mock_data, lambda x: logger.info(f"Processed: {x['id']}"))