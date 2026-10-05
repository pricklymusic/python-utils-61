# python-utils-61

A comprehensive collection of production-ready Python utility functions designed to streamline daily development tasks. This library focuses on performance, type safety, and reducing boilerplate code in data processing and system automation projects.

## Features

*   **File System Helpers:** Simplified cross-platform path manipulation and bulk file operations with built-in error handling.
*   **Data Transformation:** Efficient converters for nested dictionary flattening and complex data structure serialization.
*   **Concurrency Wrapper:** A lightweight decorator-based approach to implementing thread-safe tasks and asynchronous retries.
*   **Validation Suite:** High-performance string and object schema validators tailored for API request filtering.

## Installation

Install the package directly from PyPI:

```bash
pip install python-utils-61
```

If you prefer to install from source:

```bash
git clone https://github.com/Developer/python-utils-61.git
cd python-utils-61
pip install .
```

## Usage

Easily integrate common utility patterns into your application workflow:

```python
from pyutils61 import file_ops, data_utils

# Flatten a complex nested JSON structure
nested_data = {"user": {"id": 1, "meta": {"login": "admin"}}}
flat_data = data_utils.flatten_dict(nested_data)

# Safely create a directory tree with recursive permissions
file_ops.ensure_dir("/tmp/project/logs", mode=0o755)

print(f"Flattened keys: {list(flat_data.keys())}")
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.