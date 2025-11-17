# import subprocess
import urllib.parse

# from pathlib import Path

from downloader import initiate_download
from album_scraper import album_scraper
from scraper import url_scraper


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
            if not "/a/" in url:
                decoded_url = urllib.parse.unquote(url)
                download_url, filename = url_scraper(decoded_url)
                decoded_filename = urllib.parse.unquote(filename)
                initiate_download(download_url, decoded_filename, album_id="")
                continue
            album_id = url.split("/a/").pop()
            urls = album_scraper(url)
            if isinstance(urls, list) and len(urls) > 0:
                for url in urls:
                    decoded_url = urllib.parse.unquote(url)
                    download_url, filename = url_scraper(decoded_url)
                    decoded_filename = urllib.parse.unquote(filename)
                    initiate_download(download_url, decoded_filename, album_id=album_id)


if __name__ == "__main__":
    main()
