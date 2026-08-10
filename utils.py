import json
import datetime
import os


def save_to_json(data, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def load_from_json(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r') as json_file:
        return json.load(json_file)


def current_timestamp():
    return datetime.datetime.now().isoformat()


def flatten_list(nested_list):
    return [item for sublist in nested_list for item in sublist]


def unique_items(seq):
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]