#!/usr/bin/env python3

from scraper.email_scraper import EmailScraper

def main():
    email_scraper = EmailScraper()
    email_scraper.scrape_from_file('sites.txt', 'email-addresses.txt')

if __name__ == '__main__':
    main()