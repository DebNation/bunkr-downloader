import requests

hosts_list = [
    "https://bunkr.cr",
    "https://bunkr.pk",
    "https://bunkr.is",
    "https://bunkr.ac",
]


def is_ip_blocked(url: str) -> str:
    if "/f/" in url:
        file_id = url.split("/f/")[-1]
        diff_id_url = "/f/" + file_id
    else:
        album_id = url.split("/a/")[-1]
        diff_id_url = "/a/" + album_id

    for host in hosts_list:
        diff_url = host + diff_id_url
        try:
            response = requests.get(diff_url, timeout=5)
            if response.status_code == 200:
                return diff_url

            if response.status_code in (403, 429, 503):
                print(f"❌ Blocked on {host}")
        except Exception:
            pass

    return "NONE"
