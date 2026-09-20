import functools
import logging
from typing import Callable, Any

logging.basicConfig(level=logging.INFO)

class Pipeline:
    def __init__(self, *funcs: Callable):
        self.pipeline = funcs

    def __call__(self, initial_data: Any) -> Any:
        return functools.reduce(lambda x, f: f(x), self.pipeline, initial_data)

def sanitize(data: str) -> str:
    return data.strip().lower()

def validate(data: str) -> str:
    if not data:
        raise ValueError('empty input')
    return data

def processor(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f'executing {func.__name__}')
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f'failure in {func.__name__}: {e}')
            raise
    return wrapper

@processor
def execute_task(data: str) -> str:
    flow = Pipeline(sanitize, validate)
    return flow(data)

if __name__ == '__main__':
    print(execute_task('  PYTHON-UTILS-61  '))