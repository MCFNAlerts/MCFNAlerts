import time
from email_service.email_formatter import format_email
from email_service.sheets_reader import get_subscribers
from email_service.gmail_sender import send_email
from email_service.gmail_sender import chunk_list
from datetime import date, timedelta
import json

def main():
    try:
        with open("filtered_combined.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("No JSON found — nothing to send.")
        return

    if not data:
        print("Filtered file empty — no alerts today.")
        return
    
    print("Retrieving subscriber list...")
    subscribers = get_subscribers()
    print(f"Found {len(subscribers)} subscribers")

    print("Formatting email...")
    html_body = format_email("filtered_combined.json")
    subject = f"MCFN Daily Alert - {date.today().strftime('%B %d, %Y')}"


    if not subscribers:
        print("No subscribers found.")
        return

    # Count categories
    contributions = [item for item in data if item["Source"] == "contributions"]
    expenditures  = [item for item in data if item["Source"] == "expenditures"]
    # Decision logic
    if len(contributions) == 0 and len(expenditures) == 0:
        print("No contributions or expenditures found for this date. No emails sent.")
        return

    batches = list(chunk_list(subscribers, 499))
    print(f"Sending {len(batches)} batches...")

    for i, batch in enumerate(batches, start=1):
        try:
            send_email(batch, subject, html_body)
            print(f"Batch {i} sent! ({len(batch)} recipients)")
            time.sleep(2)  # tiny cool-down
        except Exception as e:
            print(f"Batch {i} failed: {e}")        

if __name__ == "__main__":
    main()
