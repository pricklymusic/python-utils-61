import functools

class ValidationError(Exception):
    pass

def validate_loop(schema):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            data = args[0] if args else kwargs.get('data')
            for key, expected_type in schema.items():
                val = data.get(key)
                if not isinstance(val, expected_type):
                    raise ValidationError(f'invalid type for {key}: expected {expected_type}')
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_loop({'id': int, 'payload': str})
def process_event(data):
    print(f'processing: {data['id']}')

def run_main_loop(queue):
    while True:
        try:
            item = queue.pop(0)
            process_event(item)
        except (IndexError, ValidationError, AttributeError) as e:
            print(f'skipping invalid item: {e}')
            break

if __name__ == '__main__':
    mock_queue = [{'id': 1, 'payload': 'hello'}, {'id': 'bad', 'payload': 'world'}]
    run_main_loop(mock_queue)