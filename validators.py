import functools

class ValidationError(Exception):
    pass

def validate_schema(schema):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for key, validator in schema.items():
                val = kwargs.get(key)
                if not validator(val):
                    raise ValidationError(f'Invalid value for {key}: {val}')
            return func(*args, **kwargs)
        return wrapper
    return decorator

def check_processor_loop(data_stream, schema):
    for item in data_stream:
        try:
            validate_item(item, schema)
            yield item
        except ValidationError as e:
            continue

def validate_item(item, schema):
    for key, condition in schema.items():
        if key not in item or not condition(item[key]):
            raise ValidationError(f'Validation failed at key {key}')

def is_non_empty_str(x):
    return isinstance(x, str) and len(x) > 0

def is_positive_int(x):
    return isinstance(x, int) and x > 0