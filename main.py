#!/usr/bin/env python3
"""
Email Address Scraper - Educational Tool

This script is the entry point for the email address scraper.
It demonstrates how to extract email addresses from websites for
educational purposes only.

IMPORTANT DISCLAIMER:
This tool is provided for educational purposes only. 
Before using this tool, ensure you:
1. Have permission to scrape the target websites
2. Respect robots.txt directives
3. Follow rate limiting best practices
4. Comply with all applicable laws and website Terms of Service

Improper use of web scraping tools may violate:
- Website Terms of Service
- Computer Fraud and Abuse laws
- Data protection regulations (GDPR, CCPA, etc.)
- Privacy laws

Author does not endorse or encourage any unethical or illegal use.
"""

import argparse
import sys
from scraper.email_scraper import EmailScraper

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Email Address Scraper (Educational Purposes Only)',
        epilog='Use responsibly and ethically.'
    )
    
    parser.add_argument(
        '-i', '--input',
        default='sites.txt',
        help='Input file containing URLs to scrape (one per line)'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='email-addresses.txt',
        help='Output file to save found email addresses'
    )
    
    parser.add_argument(
        '--ignore-robots',
        action='store_true',
        help='Ignore robots.txt directives (NOT RECOMMENDED)'
    )
    
    parser.add_argument(
        '--no-rate-limit',
        action='store_true',
        help='Disable rate limiting (NOT RECOMMENDED)'
    )
    
    return parser.parse_args()

def display_disclaimer():
    """Display an ethical use disclaimer and request acknowledgment"""
    print("\n" + "="*80)
    print("DISCLAIMER - EDUCATIONAL TOOL ONLY".center(80))
    print("="*80)
    print(
        "\nThis email scraping tool is for EDUCATIONAL PURPOSES ONLY.\n"
        "Improper use may violate Terms of Service, privacy laws, and data protection\n"
        "regulations such as GDPR.\n\n"
        "By proceeding, you confirm that:\n"
        "1. You have permission to scrape the websites in your input file\n"
        "2. You will respect website Terms of Service and robots.txt directives\n"
        "3. You will not use collected emails for spam or any illegal purpose\n"
        "4. You understand the legal and ethical implications of web scraping\n"
    )
    
    response = input("\nDo you understand and agree to use this tool ethically? (yes/no): ")
    if response.lower() not in ('yes', 'y'):
        print("Exiting. Please use this tool responsibly if you choose to run it again.")
        sys.exit(0)

def main():
    """Main entry point for the email scraper"""
    args = parse_args()
    
    # Display ethical use disclaimer
    display_disclaimer()
    
    # Warn if ethical controls are disabled
    if args.ignore_robots:
        print("\nWARNING: robots.txt checking is disabled. This is not recommended!")
        print("Many websites prohibit scraping in their robots.txt file.")
        
    if args.no_rate_limit:
        print("\nWARNING: Rate limiting is disabled. This may overwhelm websites!")
        print("Excessive requests can cause server strain and may be considered an attack.")
    
    # Initialize the email scraper
    email_scraper = EmailScraper(
        respect_robots=(not args.ignore_robots),
        rate_limit=(not args.no_rate_limit)
    )
    
    # Run the scraper
    email_scraper.scrape_from_file(args.input, args.output)

if __name__ == '__main__':
    main()
