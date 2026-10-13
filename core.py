"""Core pipeline composition engine with stream transformation utilities."""

from typing import Callable, Generic, Iterable, Iterator, TypeVar

I = TypeVar("I")
O = TypeVar("O")
R = TypeVar("R")


class Step(Generic[I, O]):
    """Composable transformation step supporting infix chaining via `>>`.

    Wraps stream operations to enable clean sequence processing pipelines.
    """

    def __init__(self, transform: Callable[[Iterable[I]], Iterator[O]]) -> None:
        """Initialize step with generator function over an iterable stream."""
        self._transform = transform

    def __call__(self, stream: Iterable[I]) -> Iterator[O]:
        """Apply the transformation step to an incoming data stream."""
        return self._transform(stream)

    def __rshift__(self, other: "Step[O, R]") -> "Step[I, R]":
        """Compose current step with another using the `>>` operator."""
        return Step(lambda stream: other(self(stream)))


def map_stream(fn: Callable[[I], O]) -> Step[I, O]:
    """Create a step applying `fn` to every element in the stream."""

    def _mapper(stream: Iterable[I]) -> Iterator[O]:
        for item in stream:
            yield fn(item)

    return Step(_mapper)


def filter_stream(predicate: Callable[[I], bool]) -> Step[I, I]:
    """Create a step filtering elements based on a boolean predicate."""

    def _filter(stream: Iterable[I]) -> Iterator[I]:
        for item in stream:
            if predicate(item):
                yield item

    return Step(_filter)


def batch_stream(size: int) -> Step[I, list[I]]:
    """Create a step grouping stream elements into lists of length `size`."""

    def _batcher(stream: Iterable[I]) -> Iterator[list[I]]:
        buffer: list[I] = []
        for item in stream:
            buffer.append(item)
            if len(buffer) == size:
                yield buffer
                buffer = []
        if buffer:
            yield buffer

    return Step(_batcher)
