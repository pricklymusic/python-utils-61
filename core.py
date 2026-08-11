import json
import os

class DataProcessor:
    def __init__(self, data):
        self.data = data

    def clean_data(self):
        # Remove invalid entries
        return [entry for entry in self.data if self.is_valid(entry)]

    def is_valid(self, entry):
        # Check if the entry meets criteria
        return isinstance(entry, dict) and 'value' in entry

    def aggregate_data(self):
        return sum(entry['value'] for entry in self.clean_data())

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

if __name__ == '__main__':
    file_path = os.path.join(os.getcwd(), 'data.json')
    data = read_json_file(file_path)
    processor = DataProcessor(data)
    result = processor.aggregate_data()
    print(f'Aggregate Result: {result}')