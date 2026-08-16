import json

class JSONHandler:
    def __init__(self, filename):
        self.filename = filename

    def read_data(self):
        with open(self.filename, 'r') as file:
            return json.load(file)

    def write_data(self, data):
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)

    def update_data(self, key, value):
        data = self.read_data()
        data[key] = value
        self.write_data(data)

    def delete_key(self, key):
        data = self.read_data()
        if key in data:
            del data[key]
            self.write_data(data)

# Example Usage:
if __name__ == '__main__':
    handler = JSONHandler('data.json')
    handler.write_data({'name': 'John', 'age': 30})
    handler.update_data('age', 31)
    handler.delete_key('name')
    print(handler.read_data())