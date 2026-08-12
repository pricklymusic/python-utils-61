class InputValidationError(Exception):
    pass

class Processor:
    def __init__(self, data):
        self.data = data

    def validate_input(self):
        if not isinstance(self.data, dict):
            raise InputValidationError('Input must be a dictionary.')
        if 'key' not in self.data:
            raise InputValidationError('Key not found in input dictionary.')
        if not isinstance(self.data['key'], int):
            raise InputValidationError('Value for key must be an integer.')

    def process(self):
        self.validate_input()
        return self.data['key'] * 2

if __name__ == '__main__':
    inputs = [{'key': 5}, {'key': '5'}, 'invalid_data', {'no_key': 10}]
    for input_data in inputs:
        processor = Processor(input_data)
        try:
            result = processor.process()
            print('Processed result:', result)
        except InputValidationError as e:
            print('Input validation error:', e)