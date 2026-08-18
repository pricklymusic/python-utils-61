import json
import os
import logging

class DataProcessor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = self.load_data()

    def load_data(self):
        if not os.path.exists(self.filepath):
            logging.error('File not found')
            return []
        with open(self.filepath, 'r') as file:
            return json.load(file)

    def process_data(self):
        processed = [self.clean_record(record) for record in self.data]
        return processed

    def clean_record(self, record):
        return {k: v for k, v in record.items() if v is not None}

    def save_data(self, output_filepath):
        with open(output_filepath, 'w') as file:
            json.dump(self.data, file)

if __name__ == '__main__':
    processor = DataProcessor('input_data.json')
    cleaned_data = processor.process_data()
    processor.save_data('output_data.json')