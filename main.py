import subprocess
import urllib.parse

import requests
from downloader import download_file_with_progress
from bs4 import BeautifulSoup


def album_scraper(url):
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        hrefs = [a.get("href") for a in soup.find_all("a", href=True)]  # type: ignore
        filter_urls = ["https://bunkr.cr" + str(i) for i in hrefs if "/f/" in str(i)]
        return filter_urls


with open("URLS.txt", "r") as file:
    for line in file:
        url = line.strip()
        if url == "":
            print("No URL given!")
            continue
        if "/a/" in url:
            urls = album_scraper(url)
            if isinstance(urls, list) and len(urls) > 0:
                for url in urls:
                    decoded_url = urllib.parse.unquote(url)
                    result = subprocess.run(
                        ["node", "index.js", decoded_url],
                        capture_output=True,
                        text=True,
                    )
                    filename = result.stdout.split("=")[-1].strip()
                    decoded_filename = urllib.parse.unquote(filename)
                    download_file_with_progress(result.stdout.strip(), decoded_filename)
                    continue
        decoded_url = urllib.parse.unquote(url)
        result = subprocess.run(
            ["node", "index.js", decoded_url], capture_output=True, text=True
        )
        filename = result.stdout.split("=")[-1].strip()
        decoded_filename = urllib.parse.unquote(filename)
        download_file_with_progress(result.stdout.strip(), decoded_filename)
