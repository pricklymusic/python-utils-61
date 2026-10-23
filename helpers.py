from typing import Callable, TypeVar, Generic, Any, ParamSpec
from functools import reduce, wraps

T = TypeVar("T")
R = TypeVar("R")
P = ParamSpec("P")

class MorphicPipeline(Generic[T]):
    """A fluid data-transformation tube that shuttles values through callable stages.

    Permits unconventional function chaining via bitwise OR operators (`|`) or
    direct execution calls.
    """

    def __init__(self, value: T) -> None:
        """Initialize the pipeline with a seed payload."""
        self._value: T = value

    def into(self, fn: Callable[[T], R]) -> "MorphicPipeline[R]":
        """Feed the current value into a single-arity function, yielding a new pipeline state."""
        return MorphicPipeline(fn(self._value))

    def flow(self, *steps: Callable[[Any], Any]) -> "MorphicPipeline[Any]":
        """Pass payload sequentially through an array of transformations."""
        result = reduce(lambda val, func: func(val), steps, self._value)
        return MorphicPipeline(result)

    def unwrap(self) -> T:
        """Extract the encapsulated payload from the pipeline state."""
        return self._value

    def __or__(self, fn: Callable[[T], R]) -> "MorphicPipeline[R]":
        """Syntactic sugar enabling pipeline pipe syntax."""
        return self.into(fn)

    def __repr__(self) -> str:
        """Return a textual representation of the pipeline wrapper."""
        return f"<MorphicPipeline(payload={repr(self._value)})>"


def morphic_stage(fn: Callable[P, R]) -> Callable[P, R]:
    """Decorator that tags and standardizes transformation functions for pipelines."""
    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return fn(*args, **kwargs)
    
    setattr(wrapper, "__is_morphic__", True)
    return wrapper
