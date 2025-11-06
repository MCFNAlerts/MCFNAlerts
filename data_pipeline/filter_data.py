import pandas as pd
import json
from datetime import datetime, date, timedelta
import os

DOWNLOADS_DIR = os.path.expanduser("~/Downloads")

INPUT_FILES = [
    {
        "filename": "export.xlsx",
        "source": "donations",
        "min_amount": 1000.00,
        "columns": {
            "committee": "Expending Committee Name",
            "first_name": "Payee First Name",
            "last_name_org": "Organization Name/Payee Last Name",
            "date": "Date of Expenditure",
            "amount": "Amount of Expenditure"
        }
    },
    {
        "filename": "expenditures.xlsx",
        "source": "expenditures",
        "min_amount": 5000.00,
        "columns": {
            "committee": "Filer Name",
            "first_name": "Payee First Name",
            "last_name_org": "Payee Last Name/Organization Name",
            "date": "Expenditure Date",
            "amount": "Expenditure Amount"
        }
    }
]

OUTPUT_FILE = os.path.join(DOWNLOADS_DIR, "filtered_combined.json")
TARGET_DATE = date.today() - timedelta(days=1)

def get_payee_name(row, first_name_col, last_org_col):
    first = str(row.get(first_name_col, "")).strip()
    last_org = str(row.get(last_org_col, "")).strip()
    if first and first.lower() != "nan":
        return f"{first} {last_org}".strip()
    return last_org


def process_file(file_cfg):
    results = []
    aggregated = {}
    path = os.path.join(DOWNLOADS_DIR, file_cfg["filename"])
    cols = file_cfg["columns"]
    min_amt = file_cfg["min_amount"]

    try:
        df = pd.read_excel(path)
        print(f"\nProcessing '{path}' for {file_cfg['source']} on {TARGET_DATE} (>{min_amt})...")
    except FileNotFoundError:
        print(f"File '{path}' not found, skipping.")
        return []
    except Exception as e:
        print(f"Could not read '{path}': {e}")
        return []

    for index, row in df.iterrows():
        try:
            raw_date = row[cols["date"]]
            if isinstance(raw_date, datetime):
                expenditure_date = raw_date.date()
            else:
                expenditure_date = datetime.strptime(str(raw_date), "%m/%d/%Y").date()

            amount = float(row[cols["amount"]])
            if expenditure_date == TARGET_DATE and amount > min_amt:
                committee = str(row.get(cols["committee"], "")).strip()
                payee = get_payee_name(row, cols["first_name"], cols["last_name_org"])
                key = (committee, payee)
                aggregated[key] = aggregated.get(key, 0) + amount
        except Exception as e:
            print(f"Skipping row {index} ({e})")

    for (committee, payee), total_amt in aggregated.items():
        results.append({
            "Expending Committee Name": committee,
            "Payee Name": payee,
            "Amount": round(total_amt, 2),
            "Source": file_cfg["source"]
        })

    print(f"Found {len(results)} {file_cfg['source']} transactions.")
    return results

def main():
    combined_data = []
    for cfg in INPUT_FILES:
        combined_data.extend(process_file(cfg))

    if combined_data:
        try:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(combined_data, f, indent=4)
            print(f"\nAll done! Wrote {len(combined_data)} total entries to '{OUTPUT_FILE}'.")
        except Exception as e:
            print(f"Error writing output JSON: {e}")
    else:
        print("\nNo matching records found for either file.")


if __name__ == "__main__":
    main()