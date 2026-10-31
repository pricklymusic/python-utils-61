import os
import json
import logging

class ConfigLoader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.logger = logging.getLogger(__name__)

    def load_safe(self, default=None):
        try:
            if not os.path.exists(self.filepath):
                raise FileNotFoundError(f'missing config: {self.filepath}')
            
            with open(self.filepath, 'r') as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    raise ValueError('invalid schema structure')
                return data
        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            self.logger.warning(f'fallback triggered due to: {e}')
            return default if default is not None else {}

    def get_nested(self, keys, default=None):
        config = self.load_safe()
        curr = config
        try:
            for key in keys:
                curr = curr[key]
            return curr
        except (KeyError, TypeError):
            return default

    def atomic_write(self, data):
        try:
            tmp = f'{self.filepath}.tmp'
            with open(tmp, 'w') as f:
                json.dump(data, f)
            os.replace(tmp, self.filepath)
        except Exception as e:
            self.logger.error(f'atomic write failure: {e}')
            if os.path.exists(tmp):
                os.remove(tmp)