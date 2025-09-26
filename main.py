import subprocess
import urllib.parse
from downloader import download_file_with_progress

url = input("Enter a url: ")
result = subprocess.run(["node", "index.js", url], capture_output=True, text=True)
filename = result.stdout.split("=")[-1].strip()
decoded_filename = urllib.parse.unquote(filename)
download_file_with_progress(result.stdout.strip(), decoded_filename)
