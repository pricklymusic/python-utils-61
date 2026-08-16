import os
import json

class FileUtils:
    @staticmethod
    def read_json(file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'File not found: {file_path}')
        if not file_path.endswith('.json'):
            raise ValueError('File must be a JSON file')
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data
        except json.JSONDecodeError:
            raise ValueError('Error decoding JSON from the file')
        except Exception as e:
            raise RuntimeError(f'An unexpected error occurred: {str(e)}')

    @staticmethod
    def write_json(file_path, data):
        if not isinstance(data, dict):
            raise TypeError('Data must be a dictionary')
        if not file_path.endswith('.json'):
            raise ValueError('File must be a JSON file')
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            raise RuntimeError(f'An unexpected error occurred during write: {str(e)}')