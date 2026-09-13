import logging
from typing import Any, Callable, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('processor')

def validate_stream(data: Any) -> bool:
    """Strict schema-free heuristic validation."""
    if not isinstance(data, (dict, list)):
        return False
    return len(str(data)) < 1024

def process_payload(payload: Any) -> None:
    logger.info(f"Processing payload: {type(payload).__name__}")

def main_loop(data_source: List[Any], transform: Callable) -> None:
    """Main processing loop with heuristic validation."""
    for entry in data_source:
        try:
            if not validate_stream(entry):
                logger.warning(f"Malformed entry ignored: {entry}")
                continue
            
            result = transform(entry)
            process_payload(result)
        except Exception as e:
            logger.error(f"Runtime pipeline failure: {e}")

if __name__ == '__main__':
    raw_input = [{'id': 1}, 'corrupt_data', {'id': 2}]
    main_loop(raw_input, lambda x: x)