import inspect
import weakref
from typing import Any, Callable, Dict, List, Tuple


class CleanPipeline:
    """Dynamic pipeline rebuilder that cleans and reorganizes data streams."""

    def __init__(self) -> None:
        self._stages: List[Tuple[str, Callable[[Any], Any]]] = []
        self._cache: weakref.WeakKeyDictionary = weakref.WeakKeyDictionary()

    def register(self, name: str | None = None) -> Callable:
        def decorator(func: Callable[[Any], Any]) -> Callable:
            stage_name = name or func.__name__.strip("_")
            self._stages.append((stage_name, func))
            return func

        return decorator

    def sanitize_dict(self, data: Dict[Any, Any]) -> Dict[str, Any]:
        """Deeply reorganizes nested dictionaries by stripping nulls and normalizing keys."""
        cleaned = {}
        for key, value in data.items():
            if value is None or value == "":
                continue
            norm_key = str(key).lower().strip().replace("-", "_")
            if isinstance(value, dict):
                cleaned[norm_key] = self.sanitize_dict(value)
            elif isinstance(value, (list, tuple)):
                cleaned[norm_key] = [
                    self.sanitize_dict(v) if isinstance(v, dict) else v
                    for v in value
                    if v is not None
                ]
            else:
                cleaned[norm_key] = value
        return cleaned

    def execute(self, payload: Any) -> Dict[str, Any]:
        result = self.sanitize_dict(payload) if isinstance(payload, dict) else payload
        audit_log = []

        for name, stage in self._stages:
            sig = inspect.signature(stage)
            if len(sig.parameters) == 1:
                result = stage(result)
            else:
                result = stage(result, audit_log)
            audit_log.append(f"executed:{name}")

        return {"data": result, "meta": {"pipeline_steps": audit_log}}


_global_pipe = CleanPipeline()
register_step = _global_pipe.register
run_pipeline = _global_pipe.execute
