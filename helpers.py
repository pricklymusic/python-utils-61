from typing import Any, Dict, Generic, Optional, Tuple, TypeVar
import difflib

K = TypeVar("K", bound=str)
V = TypeVar("V")


class FuzzyDict(Dict[K, V], Generic[K, V]):
    """A dictionary that recovers from key misses using string similarity.

    Attempts exact lookup first, then falls back to finding the closest
    matching string key above a specified similarity threshold.
    """

    def __init__(self, cutoff: float = 0.6, *args: Any, **kwargs: Any) -> None:
        """Initialize FuzzyDict with an optional similarity threshold."""
        super().__init__(*args, **kwargs)
        self._cutoff: float = cutoff

    def _find_closest_key(self, key: str) -> Optional[K]:
        """Locate the nearest string key in the dictionary above cutoff."""
        matches = difflib.get_close_matches(key, list(self.keys()), n=1, cutoff=self._cutoff)
        return matches[0] if matches else None

    def __getitem__(self, key: K) -> V:
        """Get item by exact key or fall back to closest fuzzy match."""
        if key in self:
            return super().__getitem__(key)

        closest = self._find_closest_key(key)
        if closest is not None:
            return super().__getitem__(closest)

        raise KeyError(
            f"Key '{key}' not found and no close matches above threshold {self._cutoff}."
        )

    def get_fuzzy(
        self, key: K, default: Optional[V] = None
    ) -> Tuple[Optional[V], float]:
        """Retrieve value alongside its match confidence score (0.0 to 1.0)."""
        if key in self:
            return super().__getitem__(key), 1.0

        closest = self._find_closest_key(key)
        if closest is not None:
            ratio = difflib.SequenceMatcher(None, key, closest).ratio()
            return super().__getitem__(closest), ratio

        return default, 0.0
