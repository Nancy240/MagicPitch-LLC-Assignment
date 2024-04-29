# Web Scrapping

This Python script allows you to scrape data from all businesses listed on https://www.yellowpages-uae.com/uae/restaurant from Yellow Pages and store it in a Google Sheet.

Prerequisites

Before running the script, make sure you have the following installed:

- Python 3.x
- Required Python packages (install via `pip install package_name`):
  - requests
  - bs4 (Beautiful Soup)
  - gspread
  - google-auth

Setup

1. Clone or download the repository to your local machine.

2. Install the required Python packages using the following command:

3. Obtain a service account JSON file from the Google Cloud Console for accessing Google Sheets API. Make sure to enable the Google Sheets API for your project.

4. Rename the service account JSON file to something meaningful (e.g., `credentials.json`) and place it in the same directory as the script.

Usage

1. Open the `yellow_pages_scraper.py` script in a text editor.

2. Update the `base_url` variable with the desired Yellow Pages URL to scrape.

3. Update the `json_path` variable with the path to your service account JSON file.

4. Optionally, adjust the `start_page`, `end_page`, and `batch_size` variables according to your requirements.

5. Run the script using the following command:

6. The script will scrape data from Yellow Pages and store it in a Google Sheet.
