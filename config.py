import json
import os

class ConfigLoader:
    def __init__(self, default_config, filepath=None):
        self.default_config = default_config
        self.filepath = filepath
        self.config = self.load_config() 

    def load_config(self):
        config = self.default_config.copy()
        if not self.filepath or not os.path.isfile(self.filepath):
            return config
        with open(self.filepath, 'r') as file:
            try:
                user_config = json.load(file)
                config.update(user_config)
            except json.JSONDecodeError:
                print('Error reading the configuration file. Using defaults.') 
        return config

    def get(self, key, default=None):
        return self.config.get(key, default)

# Example usage
if __name__ == '__main__':
    defaults = {
        'host': 'localhost',
        'port': 8000,
        'debug': False
    }
    loader = ConfigLoader(defaults, 'config.json')
    print(loader.get('host'))  # Prints host from file or defaults
