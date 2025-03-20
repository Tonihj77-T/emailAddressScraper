import re
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from .url_handler import URLHandler
from .file_handler import FileHandler

class EmailScraper:
    def __init__(self):
        self.url_handler = URLHandler()
        self.file_handler = FileHandler()
        self.email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    def extract_emails(self, html_content):
        """Extract all email addresses from HTML content using regex"""
        soup = BeautifulSoup(html_content, 'html.parser')
        # Get text content to avoid parsing HTML tags
        text = soup.get_text()
        # Find all email addresses in the text
        emails = re.findall(self.email_pattern, text)
        # Also check attributes like href="mailto:email@example.com"
        for tag in soup.find_all(href=re.compile(r'^mailto:')):
            href = tag.get('href')
            email = href.replace('mailto:', '').strip()
            if email and re.match(self.email_pattern, email):
                emails.append(email)
        return list(set(emails))  # Remove duplicates
    
    def scrape_url(self, url):
        """Scrape a single URL for email addresses"""
        try:
            html_content = self.url_handler.fetch_url(url)
            if html_content:
                return self.extract_emails(html_content)
        except Exception as e:
            print(f"Error scraping the URL: {url}: {e}")
        return []
    
    def scrape_from_file(self, input_file, output_file):
        """Scrape emails from URLs listed in input file and save to output file"""
        urls = self.file_handler.read_lines(input_file)
        all_emails = []
        
        print(f"Scraping {len(urls)} websites for email addresses...")
        for url in tqdm(urls):
            emails = self.scrape_url(url.strip())
            all_emails.extend(emails)
        
        # Remove duplicates while maintaining order
        unique_emails = []
        for email in all_emails:
            if email not in unique_emails:
                unique_emails.append(email)
        
        self.file_handler.write_lines(output_file, unique_emails)
        print(f"Found {len(unique_emails)} unique email addresses, saved to {output_file}")
