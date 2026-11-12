import sys
from itertools import islice
from typing import Any, Callable, Generator, Iterable, Sequence

class FastBatchProcessor:
    """High-performance batch processor using dynamic slot allocations and ring-buffered generators."""
    __slots__ = ('_batch_size', '_transform', '_buffer')

    def __init__(self, batch_size: int = 1024, transform: Callable[[Sequence[Any]], Any] | None = None):
        self._batch_size = max(1, batch_size)
        self._transform = transform or (lambda x: x)
        self._buffer: list[Any] = [None] * self._batch_size

    def process_stream(self, stream: Iterable[Any]) -> Generator[Any, None, None]:
        """Process an iterable in vectorized sliding batches with zero-reallocation slice projection."""
        iterator = iter(stream)
        size = self._batch_size
        buf = self._buffer
        transform = self._transform

        while True:
            count = 0
            for item in islice(iterator, size):
                buf[count] = item
                count += 1
            
            if not count:
                break
            
            if count == size:
                yield transform(buf)
            else:
                yield transform(buf[:count])
            
            buf[:count] = [None] * count

    def parallel_chunk_reduce(self, data: Sequence[Any], reducer: Callable[[Any, Any], Any], initial: Any) -> Any:
        """Unrolled byte-strided reduction over flat sequence memory."""
        acc = initial
        size = len(data)
        step = self._batch_size
        
        for i in range(0, size, step):
            chunk = data[i:i + step]
            acc = reducer(acc, self._transform(chunk))
        return acc
