import requests
import os
from datetime import date

def fetch_and_save(url, data, out_name):
    """Generic POST request for contributions and expenditures."""

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://mi-boe.entellitrak.com/",
    }

    try:
        with requests.post(url, data=data, headers=headers, timeout=60, stream=True) as resp:
            print(f"Fetching {out_name} → Status:", resp.status_code)
            resp.raise_for_status()

            ctype = resp.headers.get("content-type", "").lower()
            if "text/" in ctype or "json" in ctype:
                print(f"Unexpected non-Excel response for {out_name}:\n", resp.text[:500])
                return None

            out_dir = os.path.join(os.getcwd(), "downloads")
            os.makedirs(out_dir, exist_ok=True)
            out_path = os.path.join(out_dir, f"{out_name}.xlsx")

            with open(out_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            print(f"Saved: {out_path}")
            return out_path

    except requests.RequestException as e:
        print(f"Failed to fetch {out_name}: {e}")
        return None


if __name__ == "__main__":
    today = date.today()
    start_date = today.strftime("%Y-%m-%d")  
    start_date = "2025-10-01"

    contributions_url = (
        "https://mi-boe.entellitrak.com/etk-mi-boe-prod/page.request.do"
        "?page=page.miboeContributionPublicSearch&action=export"
    )

    contribution_data = {
        "form.contributionAmountGreaterThan": "1,000", 
        "form.contributionDateBegin": start_date,
        "form.contributionType": "individual",
    }

    fetch_and_save(contributions_url, contribution_data, "contributions")


    expenditures_url = (
        "https://mi-boe.entellitrak.com/etk-mi-boe-prod/page.request.do"
        "?page=page.miboeCommitteeExpenditureAnalysisPublicSearch&action=export"
    )

    expenditure_data = {
        "form.expenditureAmountBegin": "5,000",
        "form.expenditureDateOfExpenseBegin": start_date,
        "form.expenditureOption": "individual",
    }

    fetch_and_save(expenditures_url, expenditure_data, "expenditures")

