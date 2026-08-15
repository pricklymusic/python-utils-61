def safe_divide(numerator, denominator):
    if denominator == 0:
        raise ValueError("Denominator cannot be zero")
    return numerator / denominator


def flatten(nested_list):
    flatten_list = []
    for item in nested_list:
        if isinstance(item, list):
            flatten_list.extend(flatten(item))
        else:
            flatten_list.append(item)
    return flatten_list


def memoize(func):
    cache = {}
    def memoized_func(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return memoized_func


def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)