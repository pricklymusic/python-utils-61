from typing import Any, Callable, Dict, List, Union

class DataValidator:
    """Dynamic predicate-based schema validator for nested dicts."""
    def __init__(self, schema: Dict[str, Callable[[Any], bool]]):
        self.schema = schema

    def __call__(self, data: Dict[str, Any]) -> bool:
        return all(key in data and self.schema[key](data[key]) for key in self.schema)

    @classmethod
    def compose(cls, *validators: 'DataValidator') -> Callable[[Dict], bool]:
        return lambda data: all(v(data) for v in validators)

def type_check(t: type) -> Callable[[Any], bool]:
    return lambda val: isinstance(val, t)

def range_check(min_val: float, max_val: float) -> Callable[[Any], bool]:
    return lambda val: isinstance(val, (int, float)) and min_val <= val <= max_val

def match_regex(pattern: str) -> Callable[[Any], bool]:
    import re
    return lambda val: isinstance(val, str) and bool(re.match(pattern, val))

def validate_collection(validator: Callable[[Any], bool]) -> Callable[[Any], bool]:
    return lambda collection: isinstance(collection, (list, tuple, set)) and all(validator(item) for item in collection)

# Example usage: 
# v = DataValidator({'age': range_check(0, 120), 'tags': validate_collection(type_check(str))})
# v({'age': 25, 'tags': ['dev', 'python']}) -> True