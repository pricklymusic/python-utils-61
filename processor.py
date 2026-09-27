from typing import Any, Callable, Dict, List, Tuple

class PipeStep:
    def __init__(self, func: Callable):
        self.func = func

    def __ror__(self, left: Any) -> Any:
        if isinstance(left, tuple):
            return self.func(*left)
        if isinstance(left, dict) and getattr(self.func, "__accepts_kwargs__", False):
            return self.func(**left)
        return self.func(left)

def mark_kwargs(func: Callable) -> Callable:
    setattr(func, "__accepts_kwargs__", True)
    return func

class DataProcessor:
    def __init__(self, *steps: Callable):
        self.pipeline = [PipeStep(s) for s in steps]

    def execute(self, payload: Any) -> Any:
        data = payload
        for step in self.pipeline:
            data = data | step
        return data

    def slice_pipeline(self, start: int, stop: int) -> "DataProcessor":
        return DataProcessor(*[step.func for step in self.pipeline[start:stop]])

def clean_whitespace(val: Any) -> Any:
    if isinstance(val, str):
        return val.strip()
    if isinstance(val, dict):
        return {k: clean_whitespace(v) for k, v in val.items()}
    if isinstance(val, list):
        return [clean_whitespace(x) for x in val]
    return val

def purge_empty(val: Any) -> Any:
    if isinstance(val, dict):
        return {k: purge_empty(v) for k, v in val.items() if v not in (None, "", [], {})}
    if isinstance(val, list):
        return [purge_empty(x) for x in val if x not in (None, "", [], {})]
    return val

def normalize_keys(val: Any) -> Any:
    if isinstance(val, dict):
        return {str(k).lower().replace("-", "_"): normalize_keys(v) for k, v in val.items()}
    return val
