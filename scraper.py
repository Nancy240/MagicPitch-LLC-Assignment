import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import gspread
from google.oauth2.service_account import Credentials

def authenticate_google_sheet(json_path):
    # Authenticate using the service account JSON file
    creds = Credentials.from_service_account_file(json_path, scopes=[
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ])
    client = gspread.authorize(creds)
    return client

def scrape_yellowpages_to_sheet(base_url, worksheet, start_page=1, end_page=80, batch_size=50):
    data = [["Name", "Location", "City", "P.O. Box", "Phone", "Mobile", "Company Page Link", "Logo URL"]]
    for page_number in range(start_page, end_page + 1):
        page_url = urljoin(base_url, f'?page={page_number}')
        print(f"Scraping pages {page_number}...")

        page_response = requests.get(page_url)
        if page_response.status_code == 200:
            page_soup = BeautifulSoup(page_response.content, "html.parser")
            listings = page_soup.find_all('div', class_='row box foc')

            for listing in listings:
                name_elem = listing.find('h2', class_='cmp_name')
                name = name_elem.text.strip() if name_elem else "N/A"

                location_elem = listing.find('span', itemprop='streetAddress')
                location = location_elem.text.strip() if location_elem else "N/A"

                city_elem = listing.find('strong', itemprop='addressLocality')
                city = city_elem.text.strip() if city_elem else "N/A"

                pobox_elem = listing.find('span', class_='pobox')
                pobox = pobox_elem.text.strip() if pobox_elem else "N/A"

                phone_elems = listing.find('span', class_='phonespn')
                if phone_elems:
                    phone_elems = phone_elems.find_all('span', class_='phone')
                    phone = phone_elems[0].text.strip() if phone_elems else "N/A"
                    mobile = phone_elems[1].text.strip() if len(phone_elems) > 1 else "N/A"
                else:
                    phone = "N/A"
                    mobile = "N/A"

                company_page_link_elem = listing.find('a', title='Restaurant suppliers in UAE')
                company_page_link = urljoin(base_url, company_page_link_elem['href']) if company_page_link_elem else "N/A"

                logo_url_elem = listing.find('img', itemprop='image')
                logo_url = logo_url_elem.get('data-src') if logo_url_elem else "N/A"

                data.append([name, location, city, pobox, phone, mobile, company_page_link, logo_url])

            if page_number % batch_size == 0:
                write_to_sheet(worksheet, data)
                data = [["Name", "Location", "City", "P.O. Box", "Phone", "Mobile", "Company Page Link", "Logo URL"]]
            time.sleep(1)  # Adjust the delay as needed
        else:
            print(f"Failed to retrieve page {page_number}.")

    # Write remaining data
    if len(data) > 1:
        write_to_sheet(worksheet, data)
    print("Scraping and writing to Google Sheet completed.")

def write_to_sheet(worksheet, data):
    worksheet.append_rows(data)
    print("Data saved.")

# Specify the path to your service account JSON file
json_path = "C:\\Users\\HP PC\\Downloads\\magicpitch-llc-beed8422083c.json"

# Authenticate Google Sheet
client = authenticate_google_sheet(json_path)

# Open the Google Sheet by its title
sheet = client.open("Python Scripts")

# Select the worksheet where you want to write data
worksheet = sheet.worksheet("Sheet1")

# Define the base URL
base_url = "https://www.yellowpages-uae.com/uae/restaurant/"

# Scrape Yellow Pages and write to Google Sheet
scrape_yellowpages_to_sheet(base_url, worksheet)
