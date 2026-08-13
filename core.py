import random
import string
import json

class DataGenerator:
    def __init__(self, num_records):
        self.num_records = num_records

    def generate_record(self):
        id_length = 8
        record = {
            'id': ''.join(random.choices(string.ascii_letters + string.digits, k=id_length)),
            'value': random.randint(1, 100),
            'description': ''.join(random.choices(string.ascii_letters + ' ', k=20)).strip()
        }
        return record

    def generate_data(self):
        return [self.generate_record() for _ in range(self.num_records)]

class DataSaver:
    @staticmethod
    def save_to_json(data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

if __name__ == '__main__':
    generator = DataGenerator(num_records=10)
    data = generator.generate_data()
    DataSaver.save_to_json(data, 'output.json')
