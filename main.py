import subprocess
import urllib.parse

import requests
from downloader import initiate_download
from bs4 import BeautifulSoup
import re
import math


def album_scraper(url):
    response = requests.get(url + "?advanced=1")
    pageCount = 0
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        text = soup.find(string=re.compile(r"Files"))
        if text:
            match = re.search(r"(\d+)\s+Files", str(text))
            if match:
                file_count = int(match.group(1))
                if file_count > 100:
                    pageCount = math.ceil(file_count / 100)
    if pageCount > 0:
        print("Loading...Hold..up..")
        finalUrlsArr = []
        for page in range(pageCount):
            response = requests.get(url + f"?page={page}")
            if response.status_code == 200:
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
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            text = soup.find(string=re.compile(r"Files"))
            hrefs = [a.get("href") for a in soup.find_all("a", href=True)]  # type: ignore
            filter_urls = [
                "https://bunkr.cr" + str(i) for i in hrefs if "/f/" in str(i)
            ]
            return filter_urls


def main():
    with open("URLS.txt", "r") as file:
        contents = file.read().strip()
        if not contents:
            print("No urls found in URLS.txt")
            return 1
        for line in contents.splitlines():
            url = line.strip()
            if url == "":
                continue
            if not "bunkr" in url:
                print("Unexpected url given")
                continue
            if "https://" not in url:
                url = "https://" + url
            if "/a/" in url:
                album_id = url.split("/a/").pop()
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
                        initiate_download(
                            result.stdout.strip(), decoded_filename, album_id=album_id
                        )
                        continue
            decoded_url = urllib.parse.unquote(url)
            result = subprocess.run(
                ["node", "index.js", decoded_url], capture_output=True, text=True
            )
            filename = result.stdout.split("=")[-1].strip()
            decoded_filename = urllib.parse.unquote(filename)

            initiate_download(result.stdout.strip(), decoded_filename, album_id="")


main()
