import time
import requests

class RetryException(Exception):
    pass

def retry_request(url, retries=3, backoff=2, timeout=5):
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            attempt += 1
            if attempt == retries:
                raise RetryException(f'Request failed after {retries} attempts') from e
            time.sleep(backoff ** attempt)

if __name__ == '__main__':
    url = 'https://api.example.com/data'
    try:
        data = retry_request(url)
        print(data)
    except RetryException as e:
        print(e)