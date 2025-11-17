import base64
import re

# import time
import urllib.parse
import cloudscraper


# -------------------------------------------------------------------
# Create Cloudflare-bypassing scraper
# -------------------------------------------------------------------
scraper = cloudscraper.create_scraper(interpreter="js2py", delay=5, debug=True)


# -------------------------------------------------------------------
# Decrypt Bunkr encrypted URLs
# -------------------------------------------------------------------
def decrypt_url(base64_url: str, timestamp: int) -> str:
    binary = base64.b64decode(base64_url)

    key = f"SECRET_KEY_{timestamp // 3600}"
    key_bytes = key.encode("utf-8")

    output = bytearray()
    for i, byte in enumerate(binary):
        output.append(byte ^ key_bytes[i % len(key_bytes)])

    return output.decode("utf-8")


# -------------------------------------------------------------------
# Extract and URL-encode the title from a Bunkr page
# -------------------------------------------------------------------
def get_title(url: str) -> str | None:
    try:
        html = scraper.get(url).text

        match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE)
        if match:
            filename = match.group(1).replace(" | Bunkr", "").strip()
            return urllib.parse.quote(filename)

    except Exception as error:
        print("Error while fetching title:", error)

    return None


# -------------------------------------------------------------------
# Call Bunkr API (/api/vs)
# -------------------------------------------------------------------
def get_final_url(url: str) -> dict | None:
    try:
        slug = url.rstrip("/").split("/")[-1]
        response = scraper.post(
            "https://bunkr.cr/api/vs",
            json={"slug": slug},
            headers={"Referer": url},
        )
        return response.json()

    except Exception as error:
        print("Error calling Bunkr API:", error)

    return None


# -------------------------------------------------------------------
# Main workflow (same as your JS main())
# -------------------------------------------------------------------
def url_scraper(url: str) -> tuple[str, str]:
    # 1. Call Bunkr API
    api = get_final_url(url)
    if not api:
        raise RuntimeError(f"Failed to get API response for URL: {url}")

    # 2. Determine final URL
    encrypted = api.get("encrypted")
    if encrypted:
        try:
            final_url = decrypt_url(api["url"], api["timestamp"])
        except Exception as e:
            raise RuntimeError(f"Decryption failed: {e}")
    else:
        final_url = api.get("url")

    if not final_url:
        raise RuntimeError(f"Bunkr API did not return a valid URL for: {url}")

    # 3. Get title
    title = get_title(url)
    if not title:
        raise RuntimeError(f"Failed to extract page title from: {url}")

    # 4. Build download link
    return f"{final_url}?n={title}", title
