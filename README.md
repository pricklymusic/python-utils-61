# python-utils-61

A comprehensive collection of production-ready Python utility functions designed to streamline daily development tasks. This library bridges the gap between standard library limitations and common implementation patterns for data manipulation, file I/O, and string processing.

## Features

*   **Robust File Operations:** Simplified wrappers for directory traversal and atomic file writes to ensure data integrity during I/O operations.
*   **Data Formatting Helpers:** Specialized modules for sanitizing JSON inputs and converting complex nested dictionaries into flattened, CSV-friendly formats.
*   **Performance Decorators:** Built-in tools for easy execution timing, memoization, and automatic retry logic with exponential backoff for network requests.
*   **String Sanitization:** Efficient regex-based utilities for cleaning, slugifying, and normalizing user-provided text input.

## Installation

Install the package directly via pip:

```bash
pip install python-utils-61
```

Or, add it to your `requirements.txt`:

```text
python-utils-61>=1.0.0
```

## Usage

Import the specific utilities you need to keep your codebase clean and focused:

```python
from pyutils61.files import atomic_write
from pyutils61.decorators import retry

# Use atomic write to prevent data corruption during crashes
atomic_write("config.json", '{"status": "ok"}')

# Apply retry logic to functions prone to intermittent network failure
@retry(attempts=3, delay=2)
def fetch_data():
    # Your network logic here
    pass
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.