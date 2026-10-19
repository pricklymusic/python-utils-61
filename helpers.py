from typing import Any, Callable, Dict, List, TypeVar, Union

T = TypeVar('T')

def deep_flatten(items: Union[List[Any], tuple]) -> List[Any]:
    """
    recursive flattening of nested iterables using a generator-backed list comprehension.
    
    :param items: nested list or tuple structure
    :return: flat list of elements
    """
    def gen(current: Any):
        if isinstance(current, (list, tuple)):
            for i in current:
                yield from gen(i)
        else:
            yield current
    return list(gen(items))

def apply_pipe(value: T, functions: List[Callable[[Any], Any]]) -> Any:
    """
    serial execution of a list of functions on a single input value.
    
    :param value: starting input
    :param functions: sequence of callables
    :return: transformed output
    """
    accumulator: Any = value
    for func in functions:
        accumulator = func(accumulator)
    return accumulator

def batch_process(data: List[T], size: int) -> List[List[T]]:
    """
    chunking of data into segments of fixed length.
    
    :param data: list of items
    :param size: integer batch size
    :return: list of chunks
    """
    return [data[i:i + size] for i in range(0, len(data), size)]