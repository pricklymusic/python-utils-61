import re

class Validator:
    @staticmethod
    def validate_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_phone(phone: str) -> bool:
        pattern = r'^(\+?\d{1,3})?\s?\(?\d{1,4}?\)?[\s.-]?\d{1,4}[\s.-]?\d{1,4}[\s.-]?\d{1,9}$'
        return re.match(pattern, phone) is not None

    @staticmethod
    def validate_username(username: str) -> bool:
        pattern = r'^[a-zA-Z0-9_]{3,15}$'
        return re.match(pattern, username) is not None

    @staticmethod
    def validate_password(password: str) -> bool:
        if len(password) < 8:
            return False
        return any(char.isdigit() for char in password) and any(char.isalpha() for char in password) and any(char in '!@#$%^&*()' for char in password) 

# Example Usage
if __name__ == '__main__':
    print(Validator.validate_email('test@example.com'))  # True
    print(Validator.validate_phone('+123 456 7890'))  # True
    print(Validator.validate_username('user_name'))  # True
    print(Validator.validate_password('Passw0rd!'))  # True