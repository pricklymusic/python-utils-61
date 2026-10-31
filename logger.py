import logging
import functools

logger = logging.getLogger('python-utils-61')

def validate_inputs(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for i, arg in enumerate(args):
            if arg is None:
                logger.error(f'null argument at position {i}')
                return None
        return func(*args, **kwargs)
    return wrapper

@validate_inputs
def process_stream(data_packet):
    try:
        if not isinstance(data_packet, dict):
            raise ValueError('packet must be dictionary')
        result = f'processed: {data_packet.get("id")}'
        logger.info(result)
        return result
    except Exception as e:
        logger.critical(f'validation failure: {e}')
        return None

def main_loop(queue):
    while True:
        item = queue.get()
        if item == 'STOP':
            break
        process_stream(item)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger.info('logger initialized for processing')