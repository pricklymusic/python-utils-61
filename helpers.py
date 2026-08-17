def validate_input(data):
    if not isinstance(data, int):
        raise ValueError('Input must be an integer')
    if data < 0:
        raise ValueError('Input must be a non-negative integer')


def process_data(data):
    validate_input(data)
    # sample processing logic
    return data ** 2


def main_loop():
    while True:
        user_input = input('Enter a non-negative integer (or type "exit" to quit): ')
        if user_input.lower() == 'exit':
            break
        try:
            number = int(user_input)
            result = process_data(number)
            print(f'The result is: {result}')
        except ValueError as ve:
            print(f'Invalid input: {ve}')


if __name__ == '__main__':
    main_loop()