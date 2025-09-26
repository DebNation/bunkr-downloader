import subprocess
import urllib.parse
from downloader import download_file_with_progress

# url = input("Enter a url: ")
with open("URLS.txt", "r") as file:
    for line in file:
        if line.strip() == "":
            print("No URL given!")
            continue
        result = subprocess.run(
            ["node", "index.js", line.strip()], capture_output=True, text=True
        )
        filename = result.stdout.split("=")[-1].strip()
        decoded_filename = urllib.parse.unquote(filename)
        download_file_with_progress(result.stdout.strip(), decoded_filename)
