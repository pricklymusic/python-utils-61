from typing import Generator, Any, Callable, Dict

class ProcessingError(Exception):
    """Raised when validation fails in the processing loop."""
    pass

class LoopProcessor:
    def __init__(self) -> None:
        self.validators: Dict[str, Callable[[Any], bool]] = {}

    def register_validator(self, key: str, validator_func: Callable[[Any], bool]) -> None:
        self.validators[key] = validator_func

    def processing_loop(self) -> Generator[Dict[str, Any], Dict[str, Any], None]:
        """
        A generator-based processing loop.
        Receives data via .send(), validates it on the fly,
        and yields processed/enriched results.
        """
        # Prime the generator
        data = yield {}

        while data is not None:
            for key, validator in self.validators.items():
                if key in data:
                    val = data[key]
                    try:
                        if not validator(val):
                            raise ProcessingError(f"Field '{key}' failed validation check for value: {val}")
                    except Exception as e:
                        raise ProcessingError(f"Validation crashed on '{key}': {e}") from e
                else:
                    raise ProcessingError(f"Missing required field: '{key}'")

            processed = {f"processed_{k}": str(v).upper() for k, v in data.items()}
            data = yield processed

if __name__ == '__main__':
    processor = LoopProcessor()
    processor.register_validator('id', lambda val: isinstance(val, int) and val > 0)
    processor.register_validator('email', lambda val: isinstance(val, str) and '@' in val)

    loop = processor.processing_loop()
    next(loop)

    result = loop.send({'id': 101, 'email': 'test@example.com'})
    assert result == {'processed_id': '101', 'processed_email': 'TEST@EXAMPLE.COM'}
