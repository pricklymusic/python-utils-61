import json
import re

def is_positive_integer(value):
    try:
        ivalue = int(value)
        return ivalue > 0
    except ValueError:
        return False


def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None


def process_data(data):
    if not is_positive_integer(data.get('age')):
        raise ValueError('Age must be a positive integer.')
    if not validate_email(data.get('email')):
        raise ValueError('Invalid email address.')
    return f"Processed data for {data['name']} with age {data['age']} and email {data['email']}"


def main():
    input_data = json.loads('{"name": "John", "age": "30", "email": "john@example.com"}')
    try:
        result = process_data(input_data)
        print(result)
    except ValueError as e:
        print(e)

if __name__ == '__main__':
    main()