import os
import json
import logging

class ConfigLoader:
    def __init__(self, path):
        self.path = path
        self.cache = {}

    def load_safe(self, default_value=None):
        try:
            with open(self.path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError, PermissionError) as e:
            logging.warning(f"Configuration failure at {self.path}: {e}")
            return default_value

    def get_deep(self, key_path, default=None):
        """Access nested dictionary via dot notation string."""
        data = self.load_safe() or {}
        keys = key_path.split('.')
        for key in keys:
            if isinstance(data, dict) and key in data:
                data = data.get(key)
            else:
                return default
        return data

class ConfigRegistry:
    _instances = {}

    def __new__(cls, name):
        if name not in cls._instances:
            cls._instances[name] = super().__new__(cls)
        return cls._instances[name]

    def __init__(self, name):
        self.name = name
        self.storage = {}

    def fetch(self, key):
        try:
            return self.storage[key]
        except KeyError:
            return None

    def register(self, key, value):
        if key is None:
            raise ValueError("Registry key cannot be empty")
        self.storage[key] = value