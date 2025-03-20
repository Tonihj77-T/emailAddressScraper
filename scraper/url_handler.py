import requests
from time import sleep
import random

class URLHandler:
    def __init__(self, timeout=10, max_retries=3):
        self.timeout = timeout
        self.max_retries = max_retries
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
    
    def fetch_url(self, url):
        """Fetch HTML content from URL with retries"""
        retries = 0
        
        while retries < self.max_retries:
            try:
                response = requests.get(url, headers=self.headers, timeout=self.timeout)
                response.raise_for_status()  # Raise exception for 4XX/5XX responses
                return response.text
            except requests.exceptions.RequestException as e:
                retries += 1
                if retries >= self.max_retries:
                    raise e
                # Exponential backoff with jitter
                sleep_time = (2 ** retries) + random.uniform(0, 1)
                sleep(sleep_time)
        
        return None