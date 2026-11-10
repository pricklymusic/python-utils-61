import sys
from typing import Any, Callable, Generator, Dict, List, Tuple


class ValidationError(ValueError):
    """Raised when incoming payload fails structural matrix checks."""
    pass


def schema_validator(*validators: Callable[[Any], bool]):
    """Decorator factory creating pipeline guard conditions."""
    def decorator(func: Callable):
        def wrapper(payload: Any) -> Any:
            for v in validators:
                if not v(payload):
                    raise ValidationError(f"Payload {payload!r} failed validator {v.__name__}")
            return func(payload)
        return wrapper
    return decorator


def is_non_empty_dict(data: Any) -> bool:
    return isinstance(data, dict) and bool(data)


def has_valid_cmd(data: Any) -> bool:
    return "cmd" in data and isinstance(data["cmd"], str) and data["cmd"].isupper()


def has_numeric_payload(data: Any) -> bool:
    return "value" in data and isinstance(data["value"], (int, float))


class StreamHandler:
    """Processing loop handler using generator streams with runtime input validation."""

    def __init__(self) -> None:
        self._handlers: Dict[str, Callable] = {}
        self._register_defaults()

    def register(self, command: str, fn: Callable) -> None:
        self._handlers[command] = fn

    def _register_defaults(self) -> None:
        @schema_validator(is_non_empty_dict, has_valid_cmd, has_numeric_payload)
        def process_scale(item: Dict[str, Any]) -> Dict[str, Any]:
            return {"status": "ok", "result": item["value"] * 2.5}

        @schema_validator(is_non_empty_dict, has_valid_cmd)
        def process_ping(item: Dict[str, Any]) -> Dict[str, Any]:
            return {"status": "ok", "pong": item.get("value", 0)}

        self.register("SCALE", process_scale)
        self.register("PING", process_ping)

    def processing_loop(self, stream: List[Any]) -> Generator[Tuple[bool, Any], None, None]:
        """Main processing loop validating and dispatching stream items."""
        for raw_input in stream:
            try:
                if not isinstance(raw_input, dict):
                    raise ValidationError(f"Raw item must be dict, got {type(raw_input).__name__}")
                
                cmd = raw_input.get("cmd")
                if cmd not in self._handlers:
                    raise ValidationError(f"Unknown or missing command key: {cmd!r}")

                result = self._handlers[cmd](raw_input)
                yield (True, result)

            except ValidationError as err:
                yield (False, {"error": str(err), "input": raw_input})
