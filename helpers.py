import re
from typing import Any, Callable, Dict, List, Union


class DataLens:
    """A flexible nested data accessor and transformer using path syntax."""

    _TOKEN_REGEX = re.compile(r"([^.\[\]]+)|\[(\d+)\]")

    def __init__(self, data: Any) -> None:
        self.data = data

    def _parse_path(self, path: str) -> List[Union[str, int]]:
        tokens: List[Union[str, int]] = []
        for match in self._TOKEN_REGEX.finditer(path):
            key, idx = match.groups()
            if key is not None:
                tokens.append(key)
            elif idx is not None:
                tokens.append(int(idx))
        return tokens

    def get(self, path: str, default: Any = None) -> Any:
        """Retrieve value at path e.g. 'users[0].profile.name'."""
        curr = self.data
        for token in self._parse_path(path):
            try:
                curr = curr[token]
            except (KeyError, IndexError, TypeError):
                return default
        return curr

    def transform(self, path: str, fn: Callable[[Any], Any]) -> "DataLens":
        """Apply fn to value at path in-place and return self."""
        tokens = self._parse_path(path)
        if not tokens:
            return self

        curr = self.data
        for token in tokens[:-1]:
            curr = curr[token]

        curr[tokens[-1]] = fn(curr[tokens[-1]])
        return self

    def flatten(self) -> Dict[str, Any]:
        """Flatten nested structure into dot-notation paths."""
        flat: Dict[str, Any] = {}

        def _walk(obj: Any, prefix: str) -> None:
            if isinstance(obj, dict):
                for k, v in obj.items():
                    _walk(v, f"{prefix}.{k}" if prefix else str(k))
            elif isinstance(obj, (list, tuple)):
                for i, v in enumerate(obj):
                    _walk(v, f"{prefix}[{i}]")
            else:
                flat[prefix] = obj

        _walk(self.data, "")
        return flat
