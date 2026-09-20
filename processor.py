import difflib
from typing import Any, Mapping, Sequence

class FuzzyData:
    """
    A wrapper for dictionaries and sequences enabling resilient,
    fuzzy key matching and nested path-based traversal.
    """
    def __init__(self, data: Any, threshold: float = 0.55):
        self.data = data
        self.threshold = threshold

    def unwrap(self) -> Any:
        """Return the underlying raw data structure."""
        return self.data

    def __getitem__(self, item: Any) -> Any:
