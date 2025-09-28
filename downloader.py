from tqdm import tqdm
import requests
import os


def download_file_with_progress(url, filename):
    download_dir = "Downloads"
    os.makedirs(download_dir, exist_ok=True)
    file_path = os.path.join(download_dir, filename)

    headers = {
        "Referer": "https://bunkr.cr/",
        "User-Agent": "Wget/1.21.3 (linux-gnu)",
        "Accept": "*/*",
        "Accept-Encoding": "identity",
        "Connection": "keep-alive",
    }
    response = requests.get(url, headers=headers, stream=True)
    total_size_in_bytes = int(response.headers.get("content-length", 0))
    block_size = 1024

    progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)
    with open(file_path, "wb") as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()

    print(f"Downloaded '{filename}' from '{url}'")
