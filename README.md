[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# python-utils-61

`python-utils-61` is a lightweight, dependency-free toolkit designed to streamline everyday Python development workflows. It provides optimized helpers for robust file operations, quick data transformation, and safe environment configuration handling.

## Features

- **Atomic File Writes:** Prevent partial file corruption by writing data to temporary buffers before swapping.
- **Dot-Notation Dict Queries:** Traverse and extract values from deeply nested JSON or dictionary objects using simple path strings.
- **Human-Readable Formatting:** Quickly convert raw bytes, execution durations, and timestamps into clean display strings.
- **Typed Environment Parser:** Load environment variables directly into typed Python primitives with built-in fallback defaults.

## Installation

Install the package via `pip`:

```bash
pip install python-utils-61
```

Or install locally directly from source:

```bash
git clone https://github.com/Developer/python-utils-61.git
cd python-utils-61
pip install .
```

## Quick Start

```python
from python_utils_61 import get_env, nested_get, format_bytes

# Parse typed environment variables with defaults
max_workers = get_env("MAX_WORKERS", default=4, cast=int)

# Safely extract values from nested structures
payload = {
    "app": {
        "services": {
            "database": {"host": "localhost", "port": 5432}
        }
    }
}
db_host = nested_get(payload, "app.services.database.host", default="127.0.0.1")

# Format metrics for output
formatted_size = format_bytes(104857600)

print(f"Workers: {max_workers} | Host: {db_host} | Memory: {formatted_size}")
# Output: Workers: 4 | Host: localhost | Memory: 100.00 MB
```

## License

Distributed under the MIT License. See `LICENSE` for details.