import os
import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Function to download a file from a given URL
def download_file(url, local_filename):
    with open(local_filename, 'wb') as f:
        response = requests.get(url)
        f.write(response.content)


def extract_date_string(input_str):
    date_regex = re.compile(r'\d{5}-\d{2}-\d{2}')
    match_obj = date_regex.search(input_str)
    if match_obj:
        return match_obj.group()
    else:
        return None


# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")

# Main script
base_url = 'https://www.gov.il/he/Departments/DynamicCollectors/spokmanship_court?skip='
page = 0
documents_found = True

# Create a directory to store the downloaded files
os.makedirs('word_docs', exist_ok=True)

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)

while documents_found:
    documents_found = False
    url = base_url + str(page * 10)
    driver.get(url)
    time.sleep(5)  # Wait for the page to load

    # Get the page source
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')

    # Find all the links to Word documents
    for span in soup.find_all('span', class_='xs-pr-5 width-88 ng-binding', title=True):
        title = span['title']
        if 'קובץ' in title:
            # Remove Hebrew characters before the numbers and extract the number
            number = extract_date_string(title)

            # Construct the correct URL
            href = f'https://www.gov.il/BlobFolder/dynamiccollectorresultitem/decision{number}/he/{title}'

            documents_found = True
            print(f'Downloading {href}')
            local_filename = os.path.join('word_docs', f'{number}.docx')
            download_file(href, local_filename)

    page += 1

driver.quit()
print("Download complete!")
