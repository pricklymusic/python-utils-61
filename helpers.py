import os
import json

def read_json(file_path: str) -> dict:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    with open(file_path, 'r') as f:
        return json.load(f)


def write_json(file_path: str, data: dict) -> None:
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


def merge_dicts(dict1: dict, dict2: dict) -> dict:
    merged = dict1.copy()
    merged.update(dict2)
    return merged


def flatten_list(nested_list: list) -> list:
    return [item for sublist in nested_list for item in sublist]  


def safe_get(data: dict, key: str, default=None):
    return data.get(key, default)  


def logging_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@logging_decorator
def greet(name: str) -> str:
    return f'Hello, {name}!'