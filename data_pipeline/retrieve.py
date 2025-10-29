import requests
import os
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

currdate = datetime.today().strftime("%Y-%m-%d")
lastmonthdate = (datetime.today() - relativedelta(months=1)).strftime("%Y-%m-%d")

url = "https://mi-boe.entellitrak.com/etk-mi-boe-prod/page.request.do?page=page.miboeContributionPublicSearch&action=export"
data = {
    "form.contributionAmountGreaterThan": "1,000",        # requests will url-encode
    "form.contributionDateBegin": f"{lastmonthdate}",
    "form.contributionDateEnd": f"{currdate}",
    "form.contributionType": "individual"               
}
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Accept": "*/*",
    "Content-Type": "application/x-www-form-urlencoded",
    # Add Referer if the site expects it; adjust or remove if unnecessary
    "Referer": "https://mi-boe.entellitrak.com/",
}


def filename_from_cd(cd):
    """Extract filename from Content-Disposition header."""
    if not cd:
        return None
    m = re.search(r"filename\*=UTF-8''([^;,\n]+)", cd)
    if m:
        return m.group(1)
    m = re.search(r'filename="?([^";\n]+)"?', cd)
    return m.group(1) if m else None


def fetch_and_save():
    """POST the form, detect response type, and save file when appropriate."""
    try:
        with requests.post(url, data=data, headers=headers, timeout=60, stream=True) as resp:
            print("Status:", resp.status_code)
            resp.raise_for_status()

            ctype = resp.headers.get("content-type", "").lower()

            # JSON response (likely an API error or info)
            if "application/json" in ctype:
                try:
                    print("Response JSON:", resp.json())
                except ValueError:
                    print("Response JSON parse failed; raw text:\n", resp.text[:1000])
                return

            # Text/HTML response (likely an error page like a 403 HTML from CDN)
            if ctype.startswith("text/"):
                text = resp.text
                print("Response (text/html) snippet:\n", text[:2000])
                return

            # Otherwise assume binary file (Excel) and save
            cd = resp.headers.get("content-disposition")
            fname = filename_from_cd(cd)
            if not fname:
                if "spreadsheetml" in ctype or "xlsx" in ctype:
                    fname = "export.xlsx"
                elif "ms-excel" in ctype or "vnd.ms-excel" in ctype:
                    fname = "export.xls"
                else:
                    fname = "export.bin"

            out_dir = os.path.join(os.getcwd(), "downloads")
            os.makedirs(out_dir, exist_ok=True)
            out_path = os.path.join(out_dir, fname)
            with open(out_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print("Saved:", out_path)

    except requests.RequestException as e:
        print("Request failed:", e)


if __name__ == "__main__":
    fetch_and_save()

        