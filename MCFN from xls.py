import pandas as pd
import json
from datetime import datetime, date, timedelta

INPUT_FILE = "export.xlsx"
OUTPUT_FILE = "filtered_donations.json"
MIN_AMOUNT = 1000.00
TARGET_DATE = date.today() - timedelta(days=1)

COL_EXPENDING_COMMITTEE = "Expending Committee Name"
COL_PAYEE_FIRST_NAME = "Payee First Name"
COL_PAYEE_LAST_ORG_NAME = "Organization Name/Payee Last Name"
COL_DATE = "Date of Expenditure"
COL_AMOUNT = "Amount of Expenditure"

def get_payee_name(row):
    first_name = str(row[COL_PAYEE_FIRST_NAME]).strip()
    last_org_name = str(row[COL_PAYEE_LAST_ORG_NAME]).strip()
    
    if first_name:
        return f"{first_name} {last_org_name}"
    return last_org_name

def process_donations():
    aggregated_donations = {}

    try:
        df = pd.read_excel(INPUT_FILE)
        
        print(f"Filtering for donations on {TARGET_DATE} > {MIN_AMOUNT}...")

        for index, row in df.iterrows():
            try:
                expenditure_date_obj = row[COL_DATE]
                
                if isinstance(expenditure_date_obj, datetime):
                    expenditure_date = expenditure_date_obj.date()
                else:
                    expenditure_date = datetime.strptime(str(expenditure_date_obj), "%m/%d/%Y").date()

                amount = float(row[COL_AMOUNT])

                if expenditure_date == TARGET_DATE and amount > MIN_AMOUNT:
                    committee_name = str(row[COL_EXPENDING_COMMITTEE]).strip()
                    payee_name = get_payee_name(row)

                    aggregation_key = (committee_name, payee_name)
                    aggregated_donations[aggregation_key] = aggregated_donations.get(aggregation_key, 0) + amount

            except (ValueError, TypeError, KeyError) as e:
                print(f"Warning: Skipping row {index} due to data error: {e}.")
            except Exception as e:
                print(f"Warning: Skipping row {index} due to unexpected error: {e}.")

    except FileNotFoundError:
        print(f"Error: Input file '{INPUT_FILE}' not found.")
        return
    except ImportError:
        print(f"Error: Missing pandas or openpyxl. Please run: pip install pandas openpyxl")
        return
    except Exception as e:
        print(f"An error occurred during file reading: {e}")
        return

    output_data = []
    for (committee, payee), total_amount in aggregated_donations.items():
        output_data.append({
            "Expending Committee Name": committee,
            "Payee Name": payee,
            "Amount": round(total_amount, 2)
        })

    try:
        with open(OUTPUT_FILE, mode='w', encoding='utf-8') as outfile:
            json.dump(output_data, outfile, indent=4)
        
        print(f"\nProcessing complete.")
        print(f"Found {len(output_data)} aggregated transactions.")
        print(f"Successfully wrote filtered data to '{OUTPUT_FILE}'.")

    except IOError as e:
        print(f"Error writing to output file '{OUTPUT_FILE}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred during JSON writing: {e}")


if __name__ == "__main__":
    process_donations()
