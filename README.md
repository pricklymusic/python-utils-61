[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# python-utils-61

`python-utils-61` is a lightweight Python toolkit designed to streamline common data processing, file handling, and string manipulation tasks. It provides clean, zero-dependency helper functions to eliminate boilerplate code across everyday Python projects.

## Features

- **Safe File Operations**: Atomic JSON and text writing with automatic directory tree creation and error handling.
- **Data Structure Helpers**: Efficient utilities to flatten nested dictionaries, chunk large iterables, and perform deep dictionary merges.
- **String Transformations**: Fast converters for case formats (snake_case, camelCase, PascalCase) and robust slug generation.
- **Execution Profiling**: Simple decorators to measure function execution time and memory footprint during development.

## Installation

Install the package directly from PyPI:

```bash
pip install python-utils-61
```

Or install the latest development version directly from GitHub:

```bash
pip install git+https://github.com/Developer/python-utils-61.git
```

## Quick Start

```python
from python_utils_61.dict_utils import flatten_dict
from python_utils_61.file_utils import safe_write_json
from python_utils_61.timing import time_it

@time_it
def main():
    nested_payload = {
        "user": {
            "id": 42,
            "preferences": {
                "theme": "dark",
                "notifications": True
            }
        }
    }

    # Flatten nested structures using dot notation
    flat = flatten_dict(nested_payload)
    print(flat)
    # Output: {'user.id': 42, 'user.preferences.theme': 'dark', 'user.preferences.notifications': True}

    # Safely write data to a file, creating missing subdirectories automatically
    safe_write_json("output/user_config.json", flat, indent=2)

if __name__ == "__main__":
    main()
```

## License

Distributed under the MIT License. See `LICENSE` for more information.