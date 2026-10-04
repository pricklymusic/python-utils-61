import os
from contextlib import contextmanager

class DynamicConfig:
    """A flexible configuration loader with type-coerced env overrides and context nesting."""
    def __init__(self, **defaults):
        self.__dict__['_defaults'] = defaults
        self.__dict__['_overrides'] = {}

    def __getattr__(self, name):
        if name in self._overrides:
            return self._overrides[name]
        
        env_val = os.getenv(name.upper())
        if env_val is not None:
            default = self._defaults.get(name)
            if default is not None:
                try:
                    if isinstance(default, bool):
                        return env_val.lower() in ('true', '1', 'yes', 'on')
                    return type(default)(env_val)
                except (ValueError, TypeError):
                    pass
            return env_val

        if name in self._defaults:
            val = self._defaults[name]
            return val() if callable(val) else val
        
        raise AttributeError(f"No configuration parameter named {name}")

    def __setattr__(self, name, value):
        self._overrides[name] = value

    @contextmanager
    def context(self, **kwargs):
        """Context manager to temporarily override settings."""
        old_overrides = self._overrides.copy()
        self._overrides.update(kwargs)
        try:
            yield self
        finally:
            self._overrides.clear()
            self._overrides.update(old_overrides)
