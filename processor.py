import functools
from typing import Any, Callable, Dict, List, Union

def recursive_map(data: Any, func: Callable[[Any], Any]) -> Any:
    if isinstance(data, dict):
        return {k: recursive_map(v, func) for k, v in data.items()}
    elif isinstance(data, list):
        return [recursive_map(i, func) for i in data]
    return func(data)

def pipeline(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    return lambda x: functools.reduce(lambda acc, f: f(acc), functions, x)

class DataTransformer:
    def __init__(self, schema: Dict[str, Callable[[Any], Any]]):
        self.schema = schema

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            k: self.schema.get(k, lambda x: x)(v)
            for k, v in payload.items()
        }

def sanitize_string(val: Any) -> str:
    return str(val).strip().lower() if val is not None else ""

def dynamic_processor(data: Union[Dict, List], transformation_map: Dict[str, Callable]) -> Any:
    """
    Applies transformation logic using higher order mapping
    """
    transformer = DataTransformer(transformation_map)
    
    if isinstance(data, list):
        return [transformer.process(item) if isinstance(item, dict) else item for item in data]
    return transformer.process(data) if isinstance(data, dict) else data