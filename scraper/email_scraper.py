import re
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
from .url_handler import URLHandler
from .file_handler import FileHandler

class EmailScraper:
    """
    Email Scraper - Educational Tool
    
    This class demonstrates how emails can be extracted from websites.
    It is intended for educational purposes to understand:
    1. Web scraping mechanics
    2. HTML parsing with BeautifulSoup
    3. Regular expressions for pattern matching
    4. Ethical web scraping practices
    
    Usage of this tool should comply with website terms of service,
    privacy regulations, and ethical standards for data collection.
    """
    
    def __init__(self, respect_robots=True, rate_limit=True):
        """
        Initialize the email scraper with ethical controls
        
        Args:
            respect_robots (bool): Whether to respect robots.txt directives
            rate_limit (bool): Whether to apply rate limiting to avoid server strain
        """
        self.url_handler = URLHandler(
            timeout=10, 
            max_retries=3,
            respect_robots=respect_robots,
            rate_limit=rate_limit
        )
        self.file_handler = FileHandler()
        
        # Regular expression for finding email addresses
        # Matches local-part@domain.tld format with various allowed characters
        self.email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    def extract_emails(self, html_content):
        """
        Extract all email addresses from HTML content using regex
        
        This method demonstrates:
        1. Converting HTML to text to extract content
        2. Using regex to find patterns in text
        3. Checking HTML attributes for additional data (mailto links)
        4. Removing duplicates from results
        
        Args:
            html_content (str): HTML content to parse
            
        Returns:
            list: Unique email addresses found in the content
        """
        # Create a BeautifulSoup object to parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Get text content to avoid parsing HTML tags as email addresses
        text = soup.get_text()
        
        # Find all email addresses in the text using regex pattern
        emails = re.findall(self.email_pattern, text)
        
        # Also check mailto links which often contain email addresses
        # Example: <a href="mailto:contact@example.com">Contact Us</a>
        for tag in soup.find_all(href=re.compile(r'^mailto:')):
            href = tag.get('href')
            email = href.replace('mailto:', '').strip()
            
            # Validate extracted email with regex before adding
            if email and re.match(self.email_pattern, email):
                emails.append(email)
                
        # Remove duplicates while preserving order of discovery
        unique_emails = list(dict.fromkeys(emails))
        return unique_emails
    
    def scrape_url(self, url):
        """
        Scrape a single URL for email addresses
        
        Args:
            url (str): URL to scrape
            
        Returns:
            list: Email addresses found on the page
        """
        print(f"\nAttempting to scrape: {url}")
        print("Note: This is for educational purposes only. Ensure you have permission to scrape this site.")
        
        try:
            # Fetch the content from the URL, with built-in ethical controls
            html_content = self.url_handler.fetch_url(url)
            
            if html_content:
                emails = self.extract_emails(html_content)
                print(f"Found {len(emails)} unique email addresses")
                return emails
            else:
                print("No content was retrieved from the URL")
                
        except Exception as e:
            print(f"Error scraping the URL: {url}: {e}")
            
        return []
    
    def scrape_from_file(self, input_file, output_file):
        """
        Scrape emails from URLs listed in input file and save to output file
        
        Args:
            input_file (str): Path to file containing URLs to scrape (one per line)
            output_file (str): Path to file where found emails will be saved
        """
        # Read URLs from the input file
        urls = self.file_handler.read_lines(input_file)
        
        if not urls:
            print(f"No URLs found in {input_file} or file could not be read")
            return
            
        all_emails = []
        
        print(f"Scraping {len(urls)} websites for email addresses...")
        print("EDUCATIONAL NOTICE: Ensure you have permission to scrape these sites")
        print("and are complying with their Terms of Service.")
        
        # Add a small delay before starting to allow user to read the notice
        time.sleep(2)
        
        # Process each URL with a progress bar
        for url in tqdm(urls):
            url = url.strip()
            if not url or url.startswith('#'):  # Skip empty lines and comments
                continue
                
            # Scrape the URL for email addresses
            emails = self.scrape_url(url)
            all_emails.extend(emails)
        
        # Remove duplicates while maintaining order of discovery
        unique_emails = []
        for email in all_emails:
            if email not in unique_emails:
                unique_emails.append(email)
        
        # Write the unique emails to the output file
        success = self.file_handler.write_lines(output_file, unique_emails)
        
        if success:
            print(f"\nFound {len(unique_emails)} unique email addresses, saved to {output_file}")
            print("REMINDER: Use this data responsibly and in compliance with data protection laws.")
        else:
            print(f"\nError: Failed to save email addresses to {output_file}")
