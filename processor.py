import time
import requests
from requests.exceptions import RequestException

def retry_request(url, max_retries=3, backoff_factor=0.3):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()  # Assuming you want JSON response
        except RequestException as e:
            retries += 1
            wait_time = backoff_factor * (2 ** (retries - 1))
            print(f'Retry {retries}/{max_retries} for {url} due to {e}')
            time.sleep(wait_time)
    raise Exception(f'Max retries exceeded for {url}')

if __name__ == '__main__':
    url = 'https://api.example.com/data'
    try:
        data = retry_request(url)
        print(data)
    except Exception as e:
        print(e)