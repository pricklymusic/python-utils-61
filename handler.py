import functools
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)

class ExecutionContext:
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.registry = {}

    def register(self, name: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.registry[name] = func
            @functools.wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                if self.debug:
                    logger.info(f"Executing task: {name}")
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Task {name} failed: {e}")
                    raise
            return wrapper
        return decorator

    def run(self, name: str, *args, **kwargs) -> Any:
        target = self.registry.get(name)
        if not target:
            raise ValueError(f"No task found for {name}")
        return target(*args, **kwargs)

def create_handler(debug_mode: bool = False) -> ExecutionContext:
    return ExecutionContext(debug=debug_mode)

if __name__ == "__main__":
    manager = create_handler(debug_mode=True)
    
    @manager.register("process_data")
    def process_data(data: str) -> str:
        return f"Processed: {data}"

    result = manager.run("process_data", "sample_input")
    print(result)