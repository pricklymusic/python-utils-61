[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# python-utils-61

`python-utils-61` is a lightweight collection of production-ready Python helpers designed to streamline data transformation, file handling, and environment configuration across backend services. It eliminates repetitive boilerplate code by providing optimized, fully type-hinted utilities for everyday software development tasks.

## Features

- **Nested Dictionary Extractor:** Perform safe deep-key lookups and key-flattening on complex JSON payloads without raising `KeyError`.
- **Smart Retry Decorator:** Wrap synchronous and asynchronous functions with exponential backoff and custom exception filtering.
- **Atomic File Operations:** Read and write JSON, YAML, and plain text files safely using thread-safe locking mechanisms.
- **Environment Validator:** Parse and cast environment variables strictly at application startup with custom fallbacks.

## Installation

Install the package directly via pip:

```bash
pip install python-utils-61
```

Or install from source:

```bash
git clone https://github.com/Developer/python-utils-61.git
cd python-utils-61
pip install .
```

## Quick Start

```python
from python_utils_61 import safe_get, retry, EnvLoader

# 1. Safely extract deep values from nested dictionaries
payload = {"data": {"user": {"settings": {"theme": "dark"}}}}
theme = safe_get(payload, "data.user.settings.theme", default="light")
print(f"User theme: {theme}")

# 2. Automatically retry volatile operations
@retry(max_attempts=3, delay=1.5, exceptions=(TimeoutError, ConnectionError))
def sync_remote_data():
    # Fetch data from an external service
    return True

# 3. Load and validate environment configuration
env = EnvLoader()
db_port = env.get_int("DB_PORT", default=5432)
```

## License

Distributed under the MIT License. See `LICENSE` for more information.