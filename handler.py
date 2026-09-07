import logging

def validate_payload(data):
    if not isinstance(data, dict):
        raise ValueError('payload must be a dictionary')
    if 'id' not in data or not isinstance(data['id'], int):
        raise KeyError('missing or invalid id field')
    return True

def process_stream(input_stream):
    logger = logging.getLogger('handler')
    results = []
    for entry in input_stream:
        try:
            if validate_payload(entry):
                payload = entry.get('data', {})
                results.append({'status': 'ok', 'processed': payload})
        except (ValueError, KeyError) as e:
            logger.error(f'dropped corrupt packet: {e}')
            continue
    return results

if __name__ == '__main__':
    mock_data = [{'id': 1, 'data': 'val1'}, 'corrupt', {'id': 2, 'data': 'val2'}]
    processed = process_stream(mock_data)
    print(f'Final batch size: {len(processed)}')