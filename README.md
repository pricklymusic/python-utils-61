# python-utils-61

A comprehensive collection of production-ready Python utility functions designed to streamline daily development tasks. This library bridges common gaps in the standard library by providing robust, performance-oriented helpers for data manipulation and system operations.

## Features

*   **Robust File I/O:** Simplified context-managed helpers for recursive directory scanning and atomic file writes.
*   **Performance Decorators:** Lightweight decorators for memoization, execution time profiling, and circuit-breaker patterns.
*   **String Sanitization:** Comprehensive utilities for normalizing complex text inputs, slugification, and automated ANSI color striping.
*   **Data Structures:** Specialized wrappers for nested dictionary merging and thread-safe dictionary caching.

## Installation

Install the package directly via pip:

```bash
pip install python-utils-61
```

Or add it to your `requirements.txt`:

```text
python-utils-61>=1.0.0
```

## Basic Usage

Quickly leverage the utility decorators to profile function execution times or perform complex dictionary merges:

```python
from pyutils61 import profile_execution, merge_nested

# Profile your functions with a simple decorator
@profile_execution
def heavy_task():
    return sum(range(1000000))

# Seamlessly merge deeply nested configuration dictionaries
base_config = {"api": {"port": 80, "debug": False}}
update = {"api": {"debug": True}}

final_config = merge_nested(base_config, update)
print(final_config)
# Output: {'api': {'port': 80, 'debug': True}}
```

## Development

To contribute to this project, clone the repository and install the development dependencies:

```bash
git clone https://github.com/Developer/python-utils-61.git
cd python-utils-61
pip install -r requirements-dev.txt
pytest tests/
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.