import json
import os

class ConfigLoader:
    def __init__(self, default_config):
        self.default_config = default_config
        self.user_config = {}

    def load(self, file_path):
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                self.user_config = json.load(file)
        else:
            self.user_config = {}

    def get(self, key, default=None):
        return self.user_config.get(key, self.default_config.get(key, default))

if __name__ == '__main__':
    default = {'setting1': 'default_value1', 'setting2': 'default_value2'}
    loader = ConfigLoader(default)
    loader.load('user_config.json')
    print(loader.get('setting1'))
    print(loader.get('setting3', 'fallback_value'))
