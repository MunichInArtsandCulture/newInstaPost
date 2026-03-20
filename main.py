import os
import re
import requests
import gspread
from datetime import datetime, timezone


INSTAGRAM_URL = "https://www.instagram.com/munichartsandculture/embed"
MARKER_REGEX = r'"shortcode\\":\\"(.{11})'


def get_shortcode():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(INSTAGRAM_URL, headers=headers, timeout=30)
    response.raise_for_status()

    html = response.text
    match = re.search(MARKER_REGEX, html)

    if not match:
        raise ValueError("No shortcode found in page source.")

    return match.group(1)


def connect_to_google_sheet():
    service_account_json = os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
    spreadsheet_id = os.environ["GOOGLE_SPREADSHEET_ID"]
    worksheet_name = os.environ.get("GOOGLE_WORKSHEET_NAME", "Sheet1")

    gc = gspread.service_account_from_dict(eval(service_account_json))
    spreadsheet = gc.open_by_key(spreadsheet_id)
    worksheet = spreadsheet.worksheet(worksheet_name)

    return worksheet


def main():
    shortcode = get_shortcode()
    worksheet = connect_to_google_sheet()

    timestamp_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    worksheet.append_row([timestamp_utc, shortcode])

    print(f"Saved shortcode {shortcode} at {timestamp_utc}")


if __name__ == "__main__":
    main()
