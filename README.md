# python-utils-61

A collection of utility functions for enhancing everyday Python programming tasks. Simplify file handling, data validation, and string manipulation with these ready-to-use tools.

## Features
- **File Management Functions**: Effortlessly manage files with functions to read, write, and delete files while handling exceptions gracefully.
- **Data Validation Utilities**: Easily validate user inputs with a variety of checkers for email formats, URLs, and more.
- **String Manipulation Tools**: Quick and efficient methods for common string operations, including slug creation and case conversions.
- **Configuration Management**: Load and manage configuration settings from JSON and YAML files seamlessly.

## Installation

To install the `python-utils-61` package, simply run:

```bash
pip install python-utils-61
```

Alternatively, you can clone this repository and install it manually:

```bash
git clone https://github.com/yourusername/python-utils-61.git
cd python-utils-61
pip install .
```

## Basic Usage Example

Here's a quick example to demonstrate how to use some of the features provided by `python-utils-61`.

```python
from python_utils import file_management, data_validation, string_utils

# File Management Example
file_content = file_management.read_file('example.txt')
print(file_content)

# Data Validation Example
is_valid_email = data_validation.validate_email('user@example.com')
print(f"Is the email valid? {is_valid_email}")

# String Manipulation Example
slug = string_utils.create_slug('Hello World! This is a Test.')
print(f"Slug: {slug}")
```

## License
![MIT License](https://img.shields.io/badge/license-MIT-brightgreen)

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. 

For any issues or feature requests, please open an issue on this repository. Happy coding!