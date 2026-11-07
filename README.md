# python-utils-61

A comprehensive collection of production-ready Python utility functions designed to streamline daily development workflows. This library minimizes boilerplate code by providing robust, tested helpers for string manipulation, file system operations, and data validation.

## Features

*   **Robust Path Management**: Simplifies recursive directory traversal and file sanitization with cross-platform compatibility.
*   **Data Transformation**: High-performance helpers for nested dictionary flattening and JSON-to-YAML schema conversion.
*   **Time Utilities**: Simplified formatting for human-readable durations and ISO 8601 timestamp synchronization.
*   **Safety Wrappers**: Decorators for automated retry logic and exception handling in network-heavy operations.

## Installation

Install the package directly via pip:

```bash
pip install python-utils-61
```

For development mode, clone the repository and install requirements:

```bash
git clone https://github.com/developer/python-utils-61.git
cd python-utils-61
pip install -r requirements.txt
```

## Basic Usage

The library is designed with a flat import structure for quick integration into existing scripts.

```python
from pyutils import file_ops, text_format

# Recursively fetch all .log files
logs = file_ops.find_files(path="./logs", extension=".log")

# Sanitize input strings for safe database entry
clean_string = text_format.sanitize("  Hello, World! @2023  ")

print(f"Found {len(logs)} log files. Cleaned string: {clean_string}")
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.