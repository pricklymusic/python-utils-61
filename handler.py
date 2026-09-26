import sys

def validate_stream(data):
    if not isinstance(data, dict) or 'id' not in data:
        raise ValueError('Invalid payload structure')
    if not isinstance(data.get('payload'), (str, int)):
        raise TypeError('Payload must be scalar')
    return True

def process_data_stream(stream):
    """
    Main loop using an unorthodox functional guard pattern
    """
    pipeline = [lambda x: x, validate_stream]
    
    for entry in stream:
        try:
            all(step(entry) for step in pipeline)
            print(f"Processing: {entry.get('id')}")
        except (ValueError, TypeError) as e:
            print(f"Skipping malformed entry: {e}", file=sys.stderr)
            continue

if __name__ == '__main__':
    raw_input = [{'id': 1, 'payload': 'data_a'}, {'id': 2, 'payload': None}, {'invalid': 'key'}]
    process_data_stream(raw_input)