"""Pipeline handler module providing chainable function execution."""

from typing import TypeVar, Callable, Generic, Any, List, Optional, Tuple, Union

T = TypeVar("T")
R = TypeVar("R")


class Step(Generic[T, R]):
    """A typed wrapper around a callable representing a processing step.

    Attributes:
        func: The underlying callable to be executed.
        name: Optional descriptive label for the pipeline step.
    """

    def __init__(self, func: Callable[[T], R], name: Optional[str] = None) -> None:
        """Initialize a pipeline step with a function and optional name."""
        self.func: Callable[[T], R] = func
        self.name: str = name or getattr(func, "__name__", "anonymous")

    def __call__(self, arg: T) -> R:
        """Execute the step callable with the provided argument."""
        return self.func(arg)

    def __or__(self, next_step: Union[Callable[[R], Any], "Step[R, Any]"]) -> "PipelineHandler[T, Any]":
        """Overload bitwise OR operator to chain steps into a pipeline."""
        pipeline = PipelineHandler[T, R]([self])
        return pipeline | next_step


class PipelineHandler(Generic[T, R]):
    """A flexible pipeline handler for executing chained operations sequentially.

    Supports dynamic chaining using the bitwise OR operator.
    """

    def __init__(self, steps: Optional[List[Step[Any, Any]]] = None) -> None:
        """Initialize the handler with an optional sequence of steps."""
        self._steps: List[Step[Any, Any]] = steps or []

    def pipe(self, func: Callable[[R], Any], name: Optional[str] = None) -> "PipelineHandler[T, Any]":
        """Append a new execution step to the current pipeline."""
        step = func if isinstance(func, Step) else Step(func, name=name)
        return PipelineHandler[T, Any](self._steps + [step])

    def __or__(self, next_func: Union[Callable[[R], Any], Step[R, Any]]) -> "PipelineHandler[T, Any]":
        """Overload bitwise OR operator for pipeline composition."""
        return self.pipe(next_func if isinstance(next_func, Step) else Step(next_func))

    def process(self, initial_value: T) -> Tuple[R, List[Tuple[str, Any]]]:
        """Execute all pipeline steps sequentially on the initial value.

        Returns:
            A tuple containing the final result and an execution audit trace.
        """
        current_value: Any = initial_value
        trace: List[Tuple[str, Any]] = []

        for step in self._steps:
            current_value = step(current_value)
            trace.append((step.name, current_value))

        return current_value, trace
