# MCFN Daily Political Finance Alerts Pipeline

This repository contains the automated system used by the Michigan Campaign Finance Network (MCFN) to send daily political finance alert emails. The workflow downloads political contribution and expenditure data from the State of Michigan database, filters it, formats an email report, and sends it to all subscribers on MCFN’s mailing list. The system is designed to run automatically every day using GitHub Actions.

Features

Automatic daily runs via GitHub Actions
Bulk BCC sending compliant with Google Workspace Gmail limits
Threshold-based filtering (Contributions > $1,000, Expenditures > $5,000)
Live subscriber list integrated through Google Sheets
Fully automated end-to-end pipeline


Project Structure
MCFN/
│
├── auto_scripts/
│   └── send_daily_email.py
│
├── data_pipeline/
│   ├── retrieve_data.py
│   ├── filter_data.py
│
├── email_service/
│   ├── gmail_sender.py
│   ├── email_formatter.py
│   ├── email_template.html
│   ├── sheets_reader.py
│   ├── credentials_loader.py
│
├── downloads/
│   ├── contributions.xlsx
│   ├── expenditures.xlsx
│   
├── auto_scripts/
│   ├── daily_email.py
│   
├── .github/workflows/daily.yml
└── README.md


Required GitHub Secrets

Add the following secrets in:
GitHub → Repo Settings → Secrets and Variables → Actions

Secret Name	Description
GMAIL_SENDER	Workspace Gmail address used to send daily alerts
CREDENTIALS_JSON	Gmail OAuth client credentials (full JSON as a string)
GOOGLE_SERVICE_ACCOUNT_JSON	Google Sheets service account key JSON
SHEET_ID	Google Sheet ID containing subscribers



Credentials Setup (MCFN Must Do This After Transfer)

1. Google Sheets Access

Create a Google Cloud project
Create a service account
Generate a service account JSON key
Add JSON to GitHub secret GOOGLE_SERVICE_ACCOUNT_JSON
Share the Google Sheet with the service account email

2. Gmail API Sending

Enable Gmail API in Google Cloud
Create an OAuth 2.0 Client (Desktop type)
Download credentials.json
Add its contents to CREDENTIALS_JSON secret
Set GMAIL_SENDER to a Workspace email address
MCFN must perform the OAuth authorization once locally to generate the refresh token if needed

3. Subscriber Sheet

Set GitHub secret:
SHEET_ID=your_google_sheet_id

Daily Automation Workflow

The GitHub Actions workflow (.github/workflows/daily.yml) performs:
Pull daily XLSX data from MiBOE
Filter contributions/expenditures for the previous day
Generate filtered_combined.json
Build formatted HTML email
Read subscriber list from Google Sheets
Send email in Workspace-safe BCC batches (max 499 per batch)
Repeat daily


.gitignore

The following files must be ignored:

*.json
token.json
credentials.json
env/
downloads/
__pycache__/


Sending Logic (Bulk BCC)

Gmail allows 500 total recipients per message
One "To" address (the sender) + 499 BCC recipients
Subscribers are split into batches of 499
Each batch is sent in a single Gmail API call
A mailing list of ~1400 subscribers requires 3 batches

Transfer of Repository Ownership

MCFN must re-create all GitHub Secrets (secrets do NOT transfer)
MCFN must generate new Google credentials (OAuth + service account)

What the Code Does

Downloads contribution and expenditure reports daily
Filters transactions based on thresholds
Generates structured JSON output
Formats a modern HTML email report
Reads subscriber emails from live Google Sheets
Sends email alerts in compliant bulk batches
Runs automatically with no manual intervention

System Ready

Once secrets are configured and OAuth is completed by MCFN, the system runs fully autonomously through GitHub Actions and requires no additional maintenance.