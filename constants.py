from typing import Final

# Define constant values used throughout the application
API_URL: Final[str] = "https://api.example.com/"
TIMEOUT: Final[int] = 30
MAX_RETRIES: Final[int] = 5

# Application-specific status codes
class StatusCode:
    SUCCESS: Final[int] = 200
    NOT_FOUND: Final[int] = 404
    INTERNAL_ERROR: Final[int] = 500

# Utility constants
class Constants:
    DEFAULT_LANGUAGE: Final[str] = "en"
    SUPPORTED_LANGUAGES: Final[list[str]] = ["en", "es", "fr", "de"]
    MAX_ITEMS_PER_PAGE: Final[int] = 50

# Message templates
MESSAGE_TEMPLATES: Final[dict[str, str]] = {
    'welcome': 'Welcome to the application!',
    'goodbye': 'Thank you for using our app!'
}