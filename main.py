import urllib.parse

from utils.downloader import initiate_download
from utils.album_scraper import album_scraper
from utils.scraper import url_scraper
from utils.host_checker import is_ip_blocked


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

            diff_url = is_ip_blocked(url)
            print(diff_url)
            if diff_url == "NONE":
                return
            if not "/a/" in url:
                decoded_url = urllib.parse.unquote(diff_url)
                download_url, filename = url_scraper(decoded_url)
                decoded_filename = urllib.parse.unquote(filename)
                initiate_download(download_url, decoded_filename, album_id="")
                continue
            album_id = url.split("/a/").pop()
            urls = album_scraper(diff_url)
            if isinstance(urls, list) and len(urls) > 0:
                print(urls)
                for url in urls:
                    decoded_url = urllib.parse.unquote(url)
                    download_url, filename = url_scraper(decoded_url)
                    print(download_url)
                    decoded_filename = urllib.parse.unquote(filename)
                    initiate_download(download_url, decoded_filename, album_id=album_id)


if __name__ == "__main__":
    main()
