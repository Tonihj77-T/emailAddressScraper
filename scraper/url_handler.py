import requests
from time import sleep
import random
import urllib.robotparser
from urllib.parse import urlparse

class URLHandler:
    def __init__(self, timeout=10, max_retries=3, respect_robots=True, rate_limit=True):
        self.timeout = timeout
        self.max_retries = max_retries
        self.respect_robots = respect_robots
        self.rate_limit = rate_limit
        self.last_request_time = 0
        self.min_request_interval = 3  # Minimum seconds between requests to same domain
        
        # Use a more honest user agent that identifies the script as a scraper for educational purposes
        self.headers = {
            'User-Agent': 'Educational-Email-Scraper/1.0 (https://github.com/yourusername/email-scraper; For educational purposes only)',
        }
        
        # Keep track of domains we've visited to apply rate limiting per domain
        self.domain_last_visit = {}
        # Cache for robots.txt parsers
        self.robots_cache = {}
    
    def _can_fetch(self, url):
        """Check if scraping is allowed by robots.txt"""
        if not self.respect_robots:
            return True
            
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        scheme = parsed_url.scheme
        
        # Create robots.txt URL
        robots_url = f"{scheme}://{domain}/robots.txt"
        
        # Use cached parser if available
        if domain in self.robots_cache:
            rp = self.robots_cache[domain]
        else:
            # Initialize and cache a new parser
            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(robots_url)
            try:
                rp.read()
                self.robots_cache[domain] = rp
            except Exception as e:
                print(f"Error reading robots.txt for {domain}: {e}")
                # If we can't read robots.txt, we should be cautious and not scrape
                return False
        
        # Check if our user agent can fetch the URL
        user_agent = self.headers['User-Agent'].split('/')[0]
        can_fetch = rp.can_fetch(user_agent, url)
        
        if not can_fetch:
            print(f"robots.txt disallows scraping {url}")
            
        return can_fetch
    
    def _apply_rate_limit(self, url):
        """Apply rate limiting to avoid overwhelming servers"""
        if not self.rate_limit:
            return
            
        domain = urlparse(url).netloc
        current_time = time.time()
        
        # Wait if we've visited this domain recently
        if domain in self.domain_last_visit:
            elapsed = current_time - self.domain_last_visit[domain]
            if elapsed < self.min_request_interval:
                sleep_time = self.min_request_interval - elapsed
                print(f"Rate limiting: waiting {sleep_time:.2f} seconds before requesting {domain} again")
                sleep(sleep_time)
        
        # Update the last visit time for this domain
        self.domain_last_visit[domain] = time.time()
    
    def fetch_url(self, url):
        """Fetch HTML content from URL with retries, respecting robots.txt and rate limits"""
        # Check if we're allowed to scrape this URL
        if not self._can_fetch(url):
            return None
            
        # Apply rate limiting
        self._apply_rate_limit(url)
        
        retries = 0
        
        while retries < self.max_retries:
            try:
                print(f"Fetching {url} (attempt {retries + 1}/{self.max_retries})")
                response = requests.get(url, headers=self.headers, timeout=self.timeout)
                response.raise_for_status()  # Raise exception for 4XX/5XX responses
                return response.text
            except requests.exceptions.RequestException as e:
                retries += 1
                if retries >= self.max_retries:
                    print(f"Failed to fetch {url} after {self.max_retries} attempts: {e}")
                    raise e
                # Exponential backoff with jitter
                sleep_time = (2 ** retries) + random.uniform(0, 1)
                print(f"Request failed, retrying in {sleep_time:.2f} seconds...")
                sleep(sleep_time)
        
        return None
