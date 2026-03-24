import re
import requests
from pathlib import Path

URL = "https://www.instagram.com/munichartsandculture/embed"
OUTPUT_FILE = Path("shortcode.txt")

def get_shortcode():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(URL, headers=headers, timeout=30)
    response.raise_for_status()

    html = response.text
    match = re.search(r'"shortcode\\":\\"(.{11})', html)

    if not match:
        raise ValueError("No shortcode found")

    return match.group(1)


def main():
    shortcode = get_shortcode()
    embed_url = f"https://www.instagram.com/p/{shortcode}/embed"

    # only overwrite if changed (important for git noise)
    if OUTPUT_FILE.exists():
        existing = OUTPUT_FILE.read_text().strip()
        if existing == embed_url:
            print("No change")
            return

    OUTPUT_FILE.write_text(embed_url)
    print("Updated shortcode:", embed_url)


if __name__ == "__main__":
    main()
