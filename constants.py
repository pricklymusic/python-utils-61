from typing import Final, List

# Constants used throughout the application

# Define numeric constants
PI: Final[float] = 3.14159
EULER: Final[float] = 2.71828

# Define a list of supported file extensions
SUPPORTED_EXTENSIONS: Final[List[str]] = ['.csv', '.json', '.xml']

# Define the default timeout for network requests
DEFAULT_TIMEOUT: Final[int] = 30

# Define the maximum number of retries for network operations
MAX_RETRIES: Final[int] = 5

# Define some color constants for terminal output
class TerminalColors:
    RESET: str = '\033[0m'
    RED: str = '\033[91m'
    GREEN: str = '\033[92m'
    YELLOW: str = '\033[93m'
    BLUE: str = '\033[94m'
    MAGENTA: str = '\033[95m'
    CYAN: str = '\033[96m'

# Application-specific constants
APPLICATION_NAME: Final[str] = 'Python Utils 61'
MAX_CONNECTIONS: Final[int] = 100

# Constants for logging
LOGGING_LEVEL: Final[str] = 'DEBUG'
