import typing as t


class ValidationError(ValueError):
    pass


class LoopProcessor:
    def __init__(self, schema: t.Dict[str, t.Type]):
        self.schema = schema

    def validate_item(self, item: t.Any) -> t.Dict[str, t.Any]:
        if not isinstance(item, dict):
            raise ValidationError(f"Expected dict, got {type(item).__name__}")
        
        validated = {}
        for key, expected_type in self.schema.items():
            if key not in item:
                raise ValidationError(f"Missing required key: {key}")
            
            value = item[key]
            try:
                validated[key] = expected_type(value)
            except (ValueError, TypeError) as err:
                raise ValidationError(
                    f"Key '{key}' failed casting to {expected_type.__name__}: {err}"
                ) from err
        return validated

    def process_stream(
        self, data_stream: t.Iterable[t.Any]
    ) -> t.Generator[t.Dict[str, t.Any], None, None]:
        for raw_item in data_stream:
            try:
                validated = self.validate_item(raw_item)
                validated["_status"] = "valid"
                yield validated
            except ValidationError as exc:
                yield {
                    "_status": "invalid",
                    "_error": str(exc),
                    "_raw": raw_item,
                }