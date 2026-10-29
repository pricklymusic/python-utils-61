import logging

def validate_payload(data):
    required = {'id': int, 'payload': str}
    if not isinstance(data, dict):
        raise ValueError('non-dict input')
    for key, expected_type in required.items():
        if key not in data:
            raise KeyError(f'missing {key}')
        if not isinstance(data[key], expected_type):
            raise TypeError(f'{key} type mismatch')
    return True

def process_stream(data_stream):
    logger = logging.getLogger('processor')
    for entry in data_stream:
        try:
            if validate_payload(entry):
                result = entry['payload'].strip().upper()
                yield {'status': 'ok', 'data': result}
        except (ValueError, KeyError, TypeError) as e:
            logger.error(f'skipping invalid packet: {e}')
            continue
        except Exception as e:
            logger.critical(f'unexpected system fault: {e}')
            break

if __name__ == '__main__':
    mock_input = [{'id': 1, 'payload': 'data'}, {'id': 2, 'payload': 123}, {'id': 3, 'payload': 'valid'}]
    for item in process_stream(mock_input):
        print(item)