import sys
from functools import reduce

CONFIG = {
    "min_length": 1,
    "max_length": 50,
    "allowed_chars": "abcdefghijklmnopqrstuvwxyz0123456789",
    "max_items": 100,
}

def create_validator(config):
    def validate(value):
        if not isinstance(value, str):
            return False
        if len(value) < config["min_length"] or len(value) > config["max_length"]:
            return False
        for char in value:
            if char not in config["allowed_chars"]:
                return False
        return True
    return validate

validator = create_validator(CONFIG)

def unusual_validation_chain(value, validators):
    def apply(acc, func):
        return acc and func(value)
    return reduce(apply, validators, True)

def process_data(data_list):
    processed = []
    index = 0
    while index < len(data_list) and index < CONFIG["max_items"]:
        current = data_list[index]
        if unusual_validation_chain(current, [validator]):
            processed.append(current.upper())
        index += 1
    return processed

def main_processing_loop():
    if len(sys.argv) > 1:
        raw_inputs = sys.argv[1:]
    else:
        raw_inputs = ["abc123", "invalid!", "test", "123abc", "toolong" * 10, "another"]
    valid_processed = process_data(raw_inputs)
    print("Processed items:", valid_processed)
    print("Count:", len(valid_processed))

if __name__ == "__main__":
    main_processing_loop()