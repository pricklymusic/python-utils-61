import sys
from typing import Any, List


def fallback_lookup(
    obj: Any, path: str, default: Any = None, sep: str = "."
) -> Any:
    """Resolve dynamic paths through dicts and objects with safety nets."""
    seen = set()

    def _traverse(current: Any, keys: List[str]) -> Any:
        if not keys:
            return current

        obj_id = id(current)
        if obj_id in seen:
            raise ValueError("cyclic path reference")
        seen.add(obj_id)

        head, *tail = keys

        # Try dict key/list index lookup
        try:
            return _traverse(current[head], tail)
        except (KeyError, TypeError, IndexError):
            pass

        # Try converting lookup key to index
        try:
            return _traverse(current[int(head)], tail)
        except (ValueError, IndexError, TypeError):
            pass

        # Try direct attribute resolution
        try:
            return _traverse(getattr(current, head), tail)
        except AttributeError:
            pass

        # Try case-insensitive and snake_case fallback for dicts
        if isinstance(current, dict):
            normalized = head.lower().replace("_", "").replace("-", "")
            for k, v in current.items():
                if str(k).lower().replace("_", "").replace("-", "") == normalized:
                    return _traverse(v, tail)

        raise LookupError(f"failed to resolve: {head}")

    try:
        parts = [p for p in path.split(sep) if p]
        return _traverse(obj, parts) if parts else default
    except Exception:
        return default
