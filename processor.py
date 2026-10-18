import functools
import re
from typing import Any, Callable, List


class Step:
    """Executable pipeline step supporting bitwise shift composition."""

    def __init__(self, func: Callable):
        self.func = func
        functools.update_wrapper(self, func)

    def __call__(self, data: Any) -> Any:
        return self.func(data)

    def __rshift__(self, next_step: "Step") -> "Step":
        return Step(lambda d: next_step(self(d)))


class DataProcessor:
    """Streamlined data reorganization and sanitization engine."""

    def __init__(self) -> None:
        self._transforms: List[Step] = []

    def pipe(self, func: Callable) -> "DataProcessor":
        self._transforms.append(Step(func))
        return self

    def execute(self, payload: Any) -> Any:
        if not self._transforms:
            return payload
        pipeline = functools.reduce(lambda a, b: a >> b, self._transforms)
        return pipeline(payload)


def strip_whitespace(data: Any) -> Any:
    if isinstance(data, str):
        return data.strip()
    if isinstance(data, dict):
        return {
            (k.strip() if isinstance(k, str) else k): strip_whitespace(v)
            for k, v in data.items()
        }
    if isinstance(data, list):
        return [strip_whitespace(item) for item in data]
    return data


def normalize_keys(data: Any) -> Any:
    if isinstance(data, dict):
        cleaned = {}
        for k, v in data.items():
            new_key = re.sub(r"[-\s]+", "_", str(k)).lower()
            cleaned[new_key] = normalize_keys(v)
        return cleaned
    if isinstance(data, list):
        return [normalize_keys(item) for item in data]
    return data


def prune_empty(data: Any) -> Any:
    if isinstance(data, dict):
        pruned = {k: prune_empty(v) for k, v in data.items()}
        return {k: v for k, v in pruned.items() if v not in (None, "", {}, [])}
    if isinstance(data, list):
        pruned_list = [prune_empty(item) for item in data]
        return [item for item in pruned_list if item not in (None, "", {}, [])]
    return data
