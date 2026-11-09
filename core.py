import logging
from typing import Any, Callable, Dict

def validate_input(data: Any, schema: Dict[str, type]) -> bool:
    return isinstance(data, dict) and all(isinstance(data.get(k), v) for k, v in schema.items())

def main_process(data_stream: list, schema: Dict[str, type], task: Callable) -> None:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('processor')
    
    for entry in data_stream:
        try:
            if not validate_input(entry, schema):
                logger.warning(f"Skipping malformed entry: {entry}")
                continue
                
            result = task(entry)
            logger.info(f"Processed result: {result}")
        except Exception as e:
            logger.error(f"Execution fault on {entry}: {e}")

if __name__ == '__main__':
    schema_def = {'id': int, 'payload': str}
    data_batch = [{'id': 1, 'payload': 'test'}, {'id': 'fail', 'payload': 'oops'}, {'id': 2, 'payload': 'data'}]
    
    main_process(data_batch, schema_def, lambda x: x['payload'].upper())