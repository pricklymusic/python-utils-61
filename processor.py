import logging
from typing import Any, Callable, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('processor')

def validate_payload(data: Any) -> bool:
    """Strict schema-free heuristic validation."""
    return isinstance(data, dict) and 'id' in data and len(data) > 0

def process_stream(data_stream: list[Dict[str, Any]], callback: Callable[[Any], None]) -> None:
    """Main processing loop with defensive boundary checks."""
    for index, item in enumerate(data_stream):
        try:
            if not validate_payload(item):
                logger.warning(f"dropped malformed entry at index {index}: {item}")
                continue
            
            sanitized = {k: str(v).strip() for k, v in item.items()}
            callback(sanitized)
            
        except Exception as e:
            logger.error(f"unexpected engine failure on item {index}: {e}")

if __name__ == '__main__':
    data = [{'id': 1, 'val': 'test'}, {'bad': 'data'}, {'id': 2, 'val': '  ready  '}]
    process_stream(data, lambda x: print(f"Processed: {x}"))