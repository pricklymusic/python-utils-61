import json
import os

class ConfigLoader:
    def __init__(self, default_config_file):
        self.default_config_file = default_config_file
        self.config = self.load_defaults()

    def load_defaults(self):
        if os.path.exists(self.default_config_file):
            with open(self.default_config_file, 'r') as file:
                return json.load(file)
        return {}

    def update_config(self, new_config):
        self.config.update(new_config)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def save(self, output_file):
        with open(output_file, 'w') as file:
            json.dump(self.config, file, indent=4)

# Usage example
if __name__ == '__main__':
    loader = ConfigLoader('defaults.json')
    print(loader.get('key', 'default_value'))
    loader.update_config({'new_key': 'new_value'})
    loader.save('output.json')