import json

class ConfigurationLoader:
    def __init__(self, default_config):
        self.default_config = default_config
        self.config = default_config.copy()

    def load_from_file(self, filepath):
        try:
            with open(filepath, 'r') as file:
                file_config = json.load(file)
                self.config.update(file_config)
        except FileNotFoundError:
            print(f"Warning: Configuration file '{filepath}' not found, using defaults.")
        except json.JSONDecodeError:
            print(f"Error: Configuration file '{filepath}' is not valid JSON, using defaults.")

    def get(self, key, default=None):
        return self.config.get(key, default)

    def all(self):
        return self.config

# Example default configuration
if __name__ == '__main__':
    defaults = {
        'host': 'localhost',
        'port': 8080,
        'debug': False
    }
    config_loader = ConfigurationLoader(defaults)
    config_loader.load_from_file('config.json')
    print(config_loader.all())