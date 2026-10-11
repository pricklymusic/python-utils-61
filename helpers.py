from typing import TypeVar, Generic, Callable, Any, List

T = TypeVar('T')
U = TypeVar('U')


class LazyPipe(Generic[T]):
    """A fluent execution pipeline wrapper that defers computation until evaluation.

    Allows chaining function calls using the binary right-shift operator (>>).
    """

    def __init__(self, value: T) -> None:
        self._value: T = value
        self._steps: List[Callable[[Any], Any]] = []

    def __rshift__(self, func: Callable[[Any], U]) -> "LazyPipe[U]":
        """Registers a transformation step using the bitwise right-shift (>>) operator.

        Args:
            func: A unary callable to transform the intermediate value.

        Returns:
            A LazyPipe instance with the updated pipeline state.
        """
        new_pipe: LazyPipe[U] = LazyPipe(self._value)
        new_pipe._steps = self._steps + [func]
        return new_pipe

    def tap(self, inspector: Callable[[Any], None]) -> "LazyPipe[T]":
        """Executes a side-effect function without altering the pipeline value.

        Args:
            inspector: Callable that accepts the current pipeline state.

        Returns:
            Self with the side-effect step appended.
        """
        def _tap_wrapper(val: Any) -> Any:
            inspector(val)
            return val

        return self >> _tap_wrapper

    def resolve(self) -> Any:
        """Executes all queued transformations sequentially.

        Returns:
            The evaluated result of the entire pipeline sequence.
        """
        curr: Any = self._value
        for step in self._steps:
            curr = step(curr)
        return curr

    def __repr__(self) -> str:
        return f"LazyPipe(steps={len(self._steps)}, seed={self._value!r})"


def pipe(value: T) -> LazyPipe[T]:
    """Initializes a deferred LazyPipe pipeline with a seed value.

    Args:
        value: The starting value for subsequent transformation steps.

    Returns:
        A LazyPipe object wrapping the given seed value.
    """
    return LazyPipe(value)
