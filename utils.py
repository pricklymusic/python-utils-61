import json
import os
from datetime import datetime


def read_json(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, 'r') as file:
        return json.load(file)


def write_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def timestamped_filename(base_name, extension):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{base_name}_{timestamp}{extension}"


def flatten_list(nested_list):
    return [item for sublist in nested_list for item in sublist]


def merge_dicts(dict1, dict2):
    return {**dict1, **dict2}