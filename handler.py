import logging

class InputProcessor:
    def __init__(self):
        self.schema = {'id': int, 'payload': str}

    def validate(self, item):
        if not isinstance(item, dict):
            raise ValueError('Item must be a dictionary')
        if any(item.get(k) is None or not isinstance(item[k], v) for k, v in self.schema.items()):
            return False
        return True

    def process_loop(self, data_stream):
        for entry in data_stream:
            try:
                if self.validate(entry):
                    self.execute(entry)
                else:
                    logging.warning(f'skipped malformed entry: {entry}')
            except Exception as e:
                logging.error(f'loop failure on {entry}: {e}')

    def execute(self, item):
        print(f'processing: {item["id"]}')

def main():
    stream = [{'id': 1, 'payload': 'data'}, {'id': 'err', 'payload': 'fail'}, {'id': 2, 'payload': 'ok'}]
    handler = InputProcessor()
    handler.process_loop(stream)

if __name__ == '__main__':
    main()