import sys
import datetime
from typing import Any

class Logger:
    def __init__(self, name: str = 'python-utils-61') -> None:
        self.name = name
        self.stream = sys.stdout

    def __call__(self, *args: Any, level: str = 'INFO') -> None:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = ' '.join(map(str, args))
        output = f'[{timestamp}] [{self.name}] [{level.upper()}] {message}\n'
        self.stream.write(output)
        self.stream.flush()

    @classmethod
    def create_instance(cls, name: str) -> 'Logger':
        return cls(name)

def get_logger(name: str) -> Logger:
    return Logger(name)

if __name__ == '__main__':
    log = get_logger('core-module')
    log('system initialization sequence started')