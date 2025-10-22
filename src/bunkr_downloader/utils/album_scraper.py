import requests
from bs4 import BeautifulSoup
import re
import math


def album_scraper(url):
    response = requests.get(url + "?advanced=1")
    pageCount = 0
    if response.status_code != 200:
        print("Failed to scrape album")
        return
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.find(string=re.compile(r"Files"))
    if not text:
        print("Error: 'Files' not found in page")
        return
    match = re.search(r"(\d+)\s+Files", str(text))
    if not match:
        print("Error: Could not extract file count")
        return
    file_count = int(match.group(1))
    if file_count > 100:
        pageCount = math.ceil(file_count / 100)
    if pageCount > 0:
        print("Loading...Hold..on..")
        finalUrlsArr = []
        for page in range(pageCount):
            response = requests.get(url + f"?page={page}")
            if response.status_code != 200:
                print("Failed to scrape album")
                return
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            text = soup.find(string=re.compile(r"Files"))
            hrefs = [a.get("href") for a in soup.find_all("a", href=True)]  # type: ignore
            filter_urls = [
                "https://bunkr.cr" + str(i) for i in hrefs if "/f/" in str(i)
            ]
            finalUrlsArr = [*finalUrlsArr, *filter_urls]
        return finalUrlsArr
    else:
        response = requests.get(url)
        if response.status_code != 200:
            print("Failed to get album urls")
            return
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        text = soup.find(string=re.compile(r"Files"))
        hrefs = [a.get("href") for a in soup.find_all("a", href=True)]  # type: ignore
        filter_urls = ["https://bunkr.cr" + str(i) for i in hrefs if "/f/" in str(i)]
        return filter_urls
