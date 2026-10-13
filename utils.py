"""Functional pipeline utility for chaining transformations with operator overloading."""

from __future__ import annotations
from typing import Callable, Generic, TypeVar, Any

T = TypeVar("T")
U = TypeVar("U")


class Pipe(Generic[T]):
    """A wrapper enabling infix piping of functions using the right-shift operator (`>>`)."""

    def __init__(self, value: T) -> None:
        """Initialize the Pipe with a starting value.

        Args:
            value: The data payload to encapsulate.
        """
        self.value: T = value

    def __rshift__(self, func: Callable[[T], U]) -> Pipe[U]:
        """Apply a unary callable to the wrapped value and return a new Pipe.

        Args:
            func: Callable accepting current value and returning a new value.

        Returns:
            Pipe[U]: A new Pipe wrapping the result of `func(self.value)`.
        """
        return Pipe(func(self.value))

    def unwrap(self) -> T:
        """Extract the underlying value from the Pipe container.

        Returns:
            T: The final evaluated inner value.
        """
        return self.value

    def __repr__(self) -> str:
        """Return string representation of the Pipe container."""
        return f"Pipe({repr(self.value)})"


def tap(action: Callable[[T], Any]) -> Callable[[T], T]:
    """Create a side-effect function for pipelines without modifying payload.

    Args:
        action: Callable invoked with current payload for side effects.

    Returns:
        Callable[[T], T]: A pass-through function executing `action`.
    """
    def _tap(val: T) -> T:
        action(val)
        return val
    return _tap
