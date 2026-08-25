# python-utils-61

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

python-utils-61 is a collection of general-purpose utility functions for Python developers. It simplifies common operations such as file handling and text processing while maintaining a minimal footprint.

## Features
- Safe file writing that automatically creates missing parent directories
- String utilities for generating slugs and truncating text to specified lengths
- Functions to calculate and format time differences between dates
- Helpers for reading values from environment variables and simple config files

## Installation

```bash
pip install python-utils-61
```

## Basic Usage

```python
from python_utils_61 import file_utils, text_utils, time_utils

file_utils.write("output/reports/summary.txt", "Project summary content.")

slug = text_utils.slugify("Python Utils 61")
print(slug)

diff = time_utils.time_ago("2023-10-01")
print(diff)
```

## License

MIT License