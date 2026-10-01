import inspect
from typing import Any, Callable, Dict, Generator, Iterable, Union, get_type_hints


class AutoValidatingProcessor:
    """Main loop processor that auto-validates inputs matching target signature."""

    def __init__(self, target_function: Callable[..., Any]):
        self.target = target_function
        self.hints = get_type_hints(target_function)

    def _cast_value(self, value: Any, expected_type: Any) -> Any:
        if expected_type is bool and isinstance(value, str):
            return value.lower() in ("true", "1", "yes", "on")
        return expected_type(value)

    def validate_and_convert(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Validates payload against target function signature with conversion."""
        sig = inspect.signature(self.target)
        validated = {}
        for param_name, param in sig.parameters.items():
            if param_name not in payload:
                if param.default is inspect.Parameter.empty:
                    raise ValueError(f"Missing required parameter: {param_name}")
                validated[param_name] = param.default
                continue

            value = payload[param_name]
            expected_type = self.hints.get(param_name, Any)

            if expected_type is not Any:
                try:
                    validated[param_name] = self._cast_value(value, expected_type)
                except (TypeError, ValueError) as err:
                    raise TypeError(
                        f"Parameter '{param_name}' fails type validation for {expected_type}"
                    ) from err
            else:
                validated[param_name] = value

        return validated

    def run(
        self, stream: Iterable[Dict[str, Any]]
    ) -> Generator[Union[Any, Exception], None, None]:
        """Processes the stream in a loop, validating elements before execution."""
        for index, raw_item in enumerate(stream):
            try:
                if not isinstance(raw_item, dict):
                    raise TypeError(f"Item {index} must be a dictionary payload")
                cleaned = self.validate_and_convert(raw_item)
                yield self.target(**cleaned)
            except Exception as exc:
                yield exc
