# Email Address Scraper

A modular Python web scraper that extracts email addresses from a list of websites.

## Project Structure

```
├── main.py             # Entry point
├── requirements.txt    # Dependencies
├── sites.txt          # List of websites to scrape
└── scraper/           # Package with scraper modules
    ├── __init__.py
    ├── email_scraper.py  # Main scraper class
    ├── url_handler.py    # Handles URL fetching
    └── file_handler.py   # Handles file operations
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Add website URLs to `sites.txt` (one URL per line)
2. Run the scraper:

```bash
python main.py
```

3. The extracted email addresses will be saved to `email-addresses.txt`

## Features

- Extracts email addresses from webpage content
- Finds emails in mailto links
- Handles request errors with retries and backoff
- Shows progress with tqdm
- Removes duplicate email addresses
- Modular design for easy extension