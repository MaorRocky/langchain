import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def download_html_files(base_url, destination_folder):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a')
    print(f"Found {len(links)} links")
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for link in links:
        href = link.get('href')
        if href.endswith('.html'):
            file_url = urljoin(base_url, href)
            file_name = os.path.join(destination_folder, href)
            download_file(file_url, file_name)
            print(f"Downloaded {file_url} to {file_name}")
        else:
            print(f"Skipping {href}")

def download_file(url, file_name):
    response = requests.get(url)

    # Create the subdirectories if they don't exist
    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    with open(file_name, 'wb') as file:
        file.write(response.content)


if __name__ == "__main__":
    base_url = "https://masstransit.io/documentation/"
    destination_folder = "docs"
    download_html_files(base_url, destination_folder)
