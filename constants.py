import enum
from typing import Any, Dict, Callable

class DataSchema(enum.Enum):
    STRICT = "strict"
    LOOSE = "loose"
    AUTO = "auto"

class DataTransformer:
    """A polymorphic approach to data processing via functional mapping."""
    def __init__(self, mode: DataSchema = DataSchema.AUTO):
        self.mode = mode
        self._registry: Dict[str, Callable[[Any], Any]] = {
            "int": lambda x: int(x) if x is not None else 0,
            "str": lambda x: str(x).strip(),
            "bool": lambda x: str(x).lower() in ("true", "1", "yes")
        }

    def process(self, key: str, value: Any, target_type: str) -> Any:
        try:
            transformer = self._registry.get(target_type, lambda x: x)
            return transformer(value)
        except (ValueError, TypeError):
            if self.mode == DataSchema.STRICT:
                raise ValueError(f"Transformation failed for {key}")
            return None

    def register_hook(self, name: str, func: Callable[[Any], Any]) -> None:
        self._registry[name] = func

class GlobalState:
    VERSION = "0.6.1"
    MAX_RETRIES = 3
    SUPPORTED_TYPES = frozenset(["int", "str", "bool", "float"])
    DEFAULT_ENCODING = "utf-8"
    
def get_app_metadata() -> Dict[str, Any]:
    return {"version": GlobalState.VERSION, "ready": True}