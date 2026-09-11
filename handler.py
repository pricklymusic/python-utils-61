import collections
import functools

def deep_mapper(data, transform_func):
    """
    recursive transformation engine for nested structures
    """
    if isinstance(data, dict):
        return {k: deep_mapper(v, transform_func) for k, v in data.items()}
    elif isinstance(data, list):
        return [deep_mapper(i, transform_func) for i in data]
    return transform_func(data)

class DataPipeline:
    def __init__(self, *transformers):
        self.pipeline = transformers

    def process(self, payload):
        return functools.reduce(lambda d, f: f(d), self.pipeline, payload)

    @staticmethod
    def flatten_dict(d, parent_key='', sep='_'):
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, collections.abc.MutableMapping):
                items.extend(DataPipeline.flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    @staticmethod
    def ensure_types(mapping):
        return lambda d: {k: type(v)(d[k]) if k in d else v for k, v in mapping.items()}

def smart_cast(val):
    try:
        if str(val).lower() == 'true': return True
        if str(val).lower() == 'false': return False
        if '.' in str(val): return float(val)
        return int(val)
    except (ValueError, TypeError):
        return val