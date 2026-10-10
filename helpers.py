from typing import Any, Callable, Dict, Union


class DataLens:
    """Lightweight lens for querying and transforming nested structures."""

    def __init__(self, data: Any):
        self._data = data

    def extract(self, path: str, default: Any = None) -> Any:
        """Extract value from nested dict/list using dot-notation (e.g. 'users[0].name')."""
        curr = self._data
        tokens = path.replace("]", "").replace("[", ".").split(".")
        for token in tokens:
            if not token:
                continue
            if isinstance(curr, dict) and token in curr:
                curr = curr[token]
            elif isinstance(curr, (list, tuple)) and token.isdigit():
                idx = int(token)
                curr = curr[idx] if 0 <= idx < len(curr) else default
            else:
                return default
        return curr

    def flatten(self, sep: str = ".") -> Dict[str, Any]:
        """Flatten nested dict or list into a single-level dict with key paths."""
        flat: Dict[str, Any] = {}

        def _walk(node: Any, prefix: str = ""):
            if isinstance(node, dict):
                for k, v in node.items():
                    new_key = f"{prefix}{sep}{k}" if prefix else str(k)
                    _walk(v, new_key)
            elif isinstance(node, (list, tuple)):
                for idx, v in enumerate(node):
                    new_key = f"{prefix}[{idx}]"
                    _walk(v, new_key)
            else:
                flat[prefix] = node

        _walk(self._data)
        return flat

    def morph(self, schema: Dict[str, Union[str, Callable[[Any], Any]]]) -> Dict[str, Any]:
        """Transform data using a mapping schema of target keys to paths or functions."""
        result = {}
        for target, rule in schema.items():
            if callable(rule):
                result[target] = rule(self._data)
            elif isinstance(rule, str):
                result[target] = self.extract(rule)
        return result


def lens(data: Any) -> DataLens:
    """Factory function providing fluent access to DataLens operations."""
    return DataLens(data)
