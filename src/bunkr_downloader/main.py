import subprocess
import urllib.parse
from pathlib import Path

from .utils.downloader import initiate_download
from .utils.album_scraper import album_scraper


script_path = Path(__file__).parent / "utils" / "index.js"


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
                            [
                                "node",
                                str(script_path),
                                decoded_url,
                            ],
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
                ["node", str(script_path), decoded_url],
                capture_output=True,
                text=True,
            )
            filename = result.stdout.split("=")[-1].strip()
            decoded_filename = urllib.parse.unquote(filename)

            initiate_download(result.stdout.strip(), decoded_filename, album_id="")


if __name__ == "__main__":
    main()
