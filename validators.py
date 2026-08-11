def validate_input(data):
    if not isinstance(data, dict):
        raise ValueError('Input must be a dictionary.')
    if 'name' not in data or not isinstance(data['name'], str):
        raise ValueError('Missing or invalid name.')
    if 'age' not in data or not isinstance(data['age'], int) or data['age'] < 0:
        raise ValueError('Missing or invalid age.')
    return True

def main_processing_loop(inputs):
    for input_data in inputs:
        try:
            validate_input(input_data)
            print(f'Processing {input_data[