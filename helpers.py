import time
import requests

class RetryException(Exception):
    pass

def retry_request(url, retries=3, delay=2, backoff=2):
    """Perform a GET request with retry logic."""
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()  # Assuming we're expecting JSON
        except requests.RequestException as e:
            if attempt < retries - 1:
                time.sleep(delay)
                delay *= backoff  # Exponential backoff
            else:
                raise RetryException(f'Request failed after {retries} attempts') from e

# Example usage
# if __name__ == "__main__":
#     url = 'https://api.example.com/data'
#     try:
#         data = retry_request(url)
#         print(data)
#     except RetryException as err:
#         print(err)