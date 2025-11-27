import requests
from bs4 import BeautifulSoup
import re
import json


def album_scraper(url):
    host = url.split("/a/")[0]
    response = requests.get(url + "?advanced=1")
    pageCount = 0
    if response.status_code != 200:
        print("Failed to scrape album")
        return
    html_content = response.text
    cdn_endpoints = extract_cdn_endpoints(html_content, host)
    if not cdn_endpoints:
        print("Error: no files found in page")
        return
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.find(string=re.compile(r"Files"))
    if not text:
        print("Error: 'Files' not found in page")
        return
    match = re.search(r"(\d+)\s+Files", str(text))
    if not match:
        print("Error: Could not extract file count")
        return
    return cdn_endpoints
    # file_count = int(match.group(1))
    # print(file_count)
    # TODO: fix fetching files here;
    # if file_count > 100:
    #     pageCount = math.ceil(file_count / 100)
    # if pageCount > 0:
    #     print("Loading...Hold..on..")
    #     finalUrlsArr = []
    #     for page in range(1, pageCount + 1):
    #         response = requests.get(url + f"?page={page}")
    #         if response.status_code != 200:
    #             print("Failed to scrape album")
    #             return
    #         html_content = response.text
    #         soup = BeautifulSoup(html_content, "html.parser")
    #         text = soup.find(string=re.compile(r"Files"))
    #         hrefs = [a.get("href") for a in soup.find_all("a", href=True)]  # type: ignore
    #         print(len(hrefs))
    #         for href in hrefs:
    #             if href is not None and "/f/" in href:
    #                 finalUrlsArr.append(host + url)
    #
    #     return finalUrlsArr
    # else:
    #     response = requests.get(url)
    #     if response.status_code != 200:
    #         print("Failed to get album urls")
    #         return
    #     html_content = response.text
    #     soup = BeautifulSoup(html_content, "html.parser")
    #     text = soup.find(string=re.compile(r"Files"))
    #     hrefs = [a.get("href") for a in soup.find_all("a", href=True)]  # type: ignore
    #     finalUrlsArr = []
    #     for href in hrefs:
    #         if href is not None and "/f/" in href:
    #             finalUrlsArr.append(url)
    #
    #     return finalUrlsArr


import re
import json
from bs4 import BeautifulSoup


def extract_cdn_endpoints(html_content, host):
    soup = BeautifulSoup(html_content, "html.parser")
    prefix = host + "/f"

    for script in soup.find_all("script"):
        if script.string and "window.albumFiles" in script.string:
            script_content = script.string

            # Try JSON parsing first
            match = re.search(
                r"window\.albumFiles\s*=\s*(\[.*?\]);", script_content, re.DOTALL
            )

            if match:
                try:
                    # Parse as JSON
                    album_files = json.loads(match.group(1))
                    endpoints = [
                        item.get("cdnEndpoint")
                        for item in album_files
                        if item.get("cdnEndpoint")
                    ]

                    return [prefix + endpoint for endpoint in endpoints]

                except (json.JSONDecodeError, TypeError):
                    pass

            # Fallback to regex
            cdn_pattern = r'cdnEndpoint:\s*"([^"]+)"'
            endpoints = re.findall(cdn_pattern, script_content)

            if endpoints:
                return [prefix + endpoint for endpoint in endpoints]

    return []
