import time
import functools

# Decorator for timing function execution

def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'Execution time for {func.__name__}: {end - start:.4f} seconds')
        return result
    return wrapper

# Sample function to demonstrate optimization

@timeit
def compute_heavy_operation(n):
    total = 0
    for i in range(n):
        total += sum(j * j for j in range(1000))
    return total

# Another function that does some general processing

@timeit
def process_data(data):
    return [d * 2 for d in data if d % 2 == 0]

# Main function to showcase usage

def main():
    result = compute_heavy_operation(10)
    print(f'Result of heavy operation: {result}')
    data = range(100)
    processed = process_data(data)
    print(f'Processed data: {processed}')  

if __name__ == '__main__':
    main()