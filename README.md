# python-utils-61

A comprehensive collection of reusable Python utility functions designed to streamline daily development tasks. This library focuses on performance, readability, and minimizing boilerplate code for common data manipulation and system operations.

## Features

*   **File System Helpers:** Simplified wrappers for recursive directory traversal and intelligent file logging.
*   **Data Transformation:** Efficient tools for nested dictionary flattening and complex type conversion.
*   **Concurrency Utilities:** Thread-safe decorators and easy-to-implement rate limiters for API requests.
*   **Validation Suite:** A robust set of schema-agnostic validators for common data formats and network inputs.

## Installation

Install the package directly via pip:

```bash
pip install python-utils-61
```

Or, if you are working within a virtual environment, add it to your requirements:

```bash
echo "python-utils-61" >> requirements.txt
pip install -r requirements.txt
```

## Basic Usage

Import the utility module to handle common tasks with minimal code. Here is an example of using the file system helper:

```python
from pyutils61 import file_ops

# Recursively fetch all .json files in a directory
files = file_ops.list_files_by_extension('./data', 'json')

# Safely create nested directories
file_ops.ensure_dir('./logs/app/2023/')

print(f"Found {len(files)} files.")
```

For more complex implementations, please refer to the `examples/` directory in the repository for detailed integration patterns.

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.