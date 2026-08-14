import re
from typing import Any, Dict, Union

class InputValidator:
    def __init__(self, constraints: Dict[str, Union[type, int]]):
        self.constraints = constraints

    def validate(self, input_data: Dict[str, Any]) -> bool:
        for key, value in self.constraints.items():
            if key not in input_data:
                return False
            if isinstance(value, type):
                if not isinstance(input_data[key], value):
                    return False
            elif isinstance(value, int):
                if len(input_data[key]) != value:
                    return False
        return True

if __name__ == '__main__':
    constraints = {
        'username': str,
        'password': str,
        'age': int,
    }
    validator = InputValidator(constraints)
    input_data = {'username': 'user', 'password': 'pass123', 'age': 25}
    if validator.validate(input_data):
        print('Input is valid')
    else:
        print('Input is invalid')
