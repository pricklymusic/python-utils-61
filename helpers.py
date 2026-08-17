import json

class InputValidationError(Exception):
    pass

def validate_input(data):
    if not isinstance(data, dict):
        raise InputValidationError('Input must be a dictionary')
    required_keys = ['name', 'age', 'email']
    for key in required_keys:
        if key not in data:
            raise InputValidationError(f'Missing required key: {key}')
    if not isinstance(data['name'], str) or not data['name']:
        raise InputValidationError('Name must be a non-empty string')
    if not isinstance(data['age'], int) or data['age'] < 0:
        raise InputValidationError('Age must be a non-negative integer')
    if not isinstance(data['email'], str) or '@' not in data['email']:
        raise InputValidationError('Email must be a valid email address')

def process_data(data):
    try:
        validate_input(data)
        # Simulate processing the data
        return json.dumps({'status': 'success', 'data': data})
    except InputValidationError as e:
        return json.dumps({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    input_data = {'name': 'John Doe', 'age': 30, 'email': 'john.doe@example.com'}
    result = process_data(input_data)
    print(result)