class DataSanityError(Exception):
    """Base exception for data integrity violations."""
    def __init__(self, message, original_value=None):
        super().__init__(f"{message} | Value: {repr(original_value)}")
        self.original_value = original_value

class TransformFailure(DataSanityError):
    """Raised when data transformation pipeline collapses."""
    pass

def raise_if_none(value, label="Data"):
    if value is None:
        raise DataSanityError(f"{label} is unexpectedly void")
    return value

def context_shield(func):
    """Decorator that wraps calls in a safe exception bridge."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if isinstance(e, DataSanityError):
                raise
            raise TransformFailure("Unexpected execution halt") from e
    return wrapper

class FailureCollector:
    """Registry for suppressed errors during bulk operations."""
    def __init__(self):
        self.log = []

    def record(self, error):
        self.log.append({
            "type": type(error).__name__,
            "msg": str(error)
        })

    @property
    def has_failures(self):
        return len(self.log) > 0