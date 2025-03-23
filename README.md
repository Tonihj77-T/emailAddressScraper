# Email Address Scraper

A modular Python tool that demonstrates how to extract email addresses from websites for educational purposes.

## Disclaimer

This software is provided for **educational and research purposes only**. Before using this tool, please be aware of the following important considerations:

- **Legal Compliance**: Automated scraping of websites may violate Terms of Service of many websites. Always check and respect robots.txt files and website Terms of Service.
- **Data Protection Laws**: Collection of email addresses may be subject to data protection regulations such as GDPR in the EU. Using this tool to harvest email addresses for commercial purposes, spam, or any form of unsolicited communication is illegal in most jurisdictions.
- **Ethical Use**: The author(s) of this software do not endorse or encourage any unethical or illegal use of this tool.
- **No Warranty**: This software is provided "as is" without warranty of any kind, express or implied.

## Project Structure

```
├── main.py             # Entry point
├── requirements.txt    # Dependencies
├── sites_example.txt   # Example file (add your own URLs for testing)
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

1. Create a file named `sites.txt` with website URLs you have permission to scrape (one URL per line)
2. Run the scraper:

```bash
python main.py
```

3. The extracted email addresses will be saved to `email-addresses.txt`

## Features

- Extracts email addresses from webpage content for analysis
- Finds emails in mailto links
- Handles request errors with retries and backoff
- Shows progress with tqdm
- Removes duplicate email addresses
- Modular design for easy extension

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

## Proper Use Guidelines

1. Always obtain proper permission before scraping any website
2. Implement reasonable rate limiting to avoid server strain
3. Respect robots.txt directives and site terms of service
4. Do not use collected email addresses for spam or unsolicited communication
5. Consider the privacy implications of storing email addresses

## Contributing

Contributions that improve the educational value of this tool while emphasizing ethical use are welcome.
