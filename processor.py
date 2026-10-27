from typing import Any, Callable, Generator, Dict, List, Tuple


class ValidationError(ValueError):
    """Raised when incoming stream payload fails validation rules."""
    pass


class StreamProcessor:
    """Processes dynamic data streams with inline guardrail validations."""

    def __init__(self, rules: Dict[str, Tuple[type, Callable[[Any], bool]]]):
        self.rules = rules

    def _validate_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(record, dict):
            raise ValidationError(f"Record must be dict, received {type(record).__name__}")
        
        validated = {}
        for key, (expected_type, predicate) in self.rules.items():
            if key not in record:
                raise ValidationError(f"Missing mandatory field: {key}")
            val = record[key]
            if not isinstance(val, expected_type):
                raise ValidationError(f"Field '{key}' type mismatch: expected {expected_type.__name__}")
            if not predicate(val):
                raise ValidationError(f"Field '{key}' failed domain predicate check: {val!r}")
            validated[key] = val
        return validated

    def run_pipeline(self, raw_stream: List[Any]) -> Generator[Dict[str, Any], None, None]:
        """Main processing loop consuming stream with validation handling."""
        for idx, item in enumerate(raw_stream):
            try:
                clean_item = self._validate_record(item)
                yield {**clean_item, "_seq": idx, "_status": "VALID"}
            except ValidationError as exc:
                yield {"_seq": idx, "_status": "REJECTED", "_error": str(exc)}


def create_default_processor() -> StreamProcessor:
    return StreamProcessor({
        "id": (int, lambda x: x > 0),
        "name": (str, lambda x: len(x.strip()) > 0),
        "score": ((int, float), lambda x: 0 <= x <= 100),
    })
