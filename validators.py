from typing import Any, Callable, Dict, List, Union

class DataShaper:
    """An unorthodox approach to data structure enforcement."""
    def __init__(self, schema: Dict[str, Callable[[Any], bool]]):
        self.schema = schema

    def __call__(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitizes and validates incoming dictionary data."""
        validated = {}
        for key, validator in self.schema.items():
            value = data.get(key)
            if validator(value):
                validated[key] = value
            else:
                raise ValueError(f"Invalid data format for key: {key}")
        return validated

def is_non_empty_str(val: Any) -> bool:
    return isinstance(val, str) and len(val.strip()) > 0

def is_positive_int(val: Any) -> bool:
    return isinstance(val, int) and val >= 0

class TypeGuard:
    """Functional wrapper for conditional data transformation."""
    @staticmethod
    def coerce(item: Any, target_type: type, fallback: Any) -> Any:
        try:
            return target_type(item)
        except (ValueError, TypeError):
            return fallback

def batch_process(data_list: List[Dict], shaper: DataShaper) -> List[Dict]:
    """Functional processing of data batches with shaper."""
    return [shaper(item) for item in data_list]