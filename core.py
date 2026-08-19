import json
import os

def load_json(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found")
    with open(file_path, 'r') as f:
        return json.load(f)

def save_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

class DataProcessor:
    def __init__(self, data):
        self.data = data

    def filter(self, condition):
        return [item for item in self.data if condition(item)]

    def transform(self, func):
        return [func(item) for item in self.data]

def main():
    data = load_json('input.json')
    processor = DataProcessor(data)
    filtered_data = processor.filter(lambda x: x['active'])
    transformed_data = processor.transform(lambda x: x['name'].upper())
    save_json(transformed_data, 'output.json')

if __name__ == '__main__':
    main()