import functools
from typing import Callable, Dict, Type, Tuple, Any

class ResilientBridge:
    """An unusual recovery mechanism that intercepts exceptions and mutates inputs
    to retry execution instead of failing immediately.
    """
    def __init__(self):
        self._strategies: Dict[Type[BaseException], Callable[..., Tuple[tuple, dict]]] = {}

    def register_strategy(self, exc_type: Type[BaseException], strategy: Callable[..., Tuple[tuple, dict]]):
        """Register an argument-healing strategy for a specific exception class."""
        self._strategies[exc_type] = strategy

    def __call__(self, func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                strategy = None
                for exc_t, strat in self._strategies.items():
                    if isinstance(e, exc_t):
                        strategy = strat
                        break
                
                if not strategy:
                    raise e
                
                try:
                    new_args, new_kwargs = strategy(*args, **kwargs)
                except Exception as strategy_err:
                    raise RuntimeError("Failed to resolve exception using registered strategy") from strategy_err
                
                return func(*new_args, **new_kwargs)
        return wrapper

def zero_division_healer(*args, **kwargs) -> Tuple[tuple, dict]:
    """Replaces numerical zeros with a tiny float value to prevent ZeroDivisionError."""
    new_args = tuple(1e-9 if val == 0 else val for val in args)
    new_kwargs = {k: (1e-9 if v == 0 else v) for k, v in kwargs.items()}
    return new_args, new_kwargs

def type_error_string_coercion(*args, **kwargs) -> Tuple[tuple, dict]:
    """Attempts to stringify elements when a TypeError occurs during string ops."""
    new_args = tuple(str(val) if val is not None else "" for val in args)
    new_kwargs = {k: (str(v) if v is not None else "") for k, v in kwargs.items()}
    return new_args, new_kwargs

default_bridge = ResilientBridge()
default_bridge.register_strategy(ZeroDivisionError, zero_division_healer)
default_bridge.register_strategy(TypeError, type_error_string_coercion)
