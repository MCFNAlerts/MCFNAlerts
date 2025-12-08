# MCFN Daily Political Finance Alerts Pipeline

This repository contains the automated system used by the Michigan Campaign Finance Network (MCFN) to send daily political finance alert emails. The pipeline downloads political contribution and expenditure data from the Michigan Bureau of Elections (MiBOE), filters it, formats a daily summary, and emails the report to all subscribers on the MCFN mailing list. The system runs automatically each day using GitHub Actions.


## Features

- Automatic daily execution via GitHub Actions
- Bulk BCC sending compliant with Google Workspace Gmail limits
- Threshold-based filtering (Contributions over $1,000; Expenditures over $5,000)
- Live subscriber list integrated through Google Sheets
- Fully automated end-to-end pipeline

## What the Code Does

- Downloads daily contribution and expenditure data
- Filters records above required reporting thresholds
- Produces a structured JSON output
- Formats a professional HTML email summary
- Retrieves subscriber emails from Google Sheets
- Sends the report via the Gmail API
- Runs automatically through GitHub Actions every day

  # Daily Automation Workflow

The GitHub Actions workflow (.github/workflows/daily.yml) performs the following:

1. Download daily XLSX reports for contributions and expenditures
2. Filter transactions for the previous day using defined thresholds
3. Produce "filtered_combined.json"
4. Generate the formatted HTML email summary
5. Retrieve the subscriber list from Google Sheets
6. Send emails in BCC batches (maximum 499 recipients per batch)
7. Repeat automatically every day

## Email Sending Logic (Bulk BCC)

- Gmail allows a maximum of 500 total recipients per message
- The system sends one "To" address (the sender)
- Up to 499 subscribers are placed in BCC

If more than 499 subscribers exist, the list is automatically split into batches.
For example, 1,400 subscribers results in three separate batched emails.


## Transfer of Repository Ownership

When transferring ownership to MCFN:

- GitHub Secrets must be recreated by MCFN because secrets do not transfer
- New Google credentials must be generated (OAuth2 and Service Account)
- The service account must be given access to the subscriber Google Sheet

Once configured, the system runs entirely without manual maintenance.

## Credentials Setup (Performed by MCFN After Repository Transfer)

### 1. Google Sheets Access (Service Account)

- Create or select a Google Cloud project
- Create a service account
- Generate a service account JSON key
- Add the JSON contents to the "GOOGLE_SERVICE_ACCOUNT_JSON" GitHub secret
- Share the subscriber Google Sheet with the service account email address

### 2. Gmail API Access (OAuth2)

- Enable the Gmail API in the Google Cloud project
- Create an OAuth 2.0 Desktop Client
- Download the OAuth credentials.json
- Add its full content to the "CREDENTIALS_JSON" GitHub secret
- Set GMAIL_SENDER to the Gmail/Workspace sending address
- MCFN must run the OAuth authorization once locally if a refresh token is required

### 3. Mailing List

Set the GitHub secret:
SHEET_ID = your_google_sheet_id

Create a Google Form with 2 questions:
1. 'Email Address' as short answer text
2. 'Action' as dropdown with 2 options (1. Subscribe, 2. Unsubscribe)
3. Navigate to the responses tab of the form and click 'View in Sheets'
4. Create another spreadsheet WITHIN this form project (click the + in the bottom left of footer)
5. Title this page 'ActiveSubscribers"
6. In cell A1, paste this formula:
````
  =LET(
  responses, 'Form Responses 1'!A2:C,
  emails, INDEX(responses,,2),
  actions, INDEX(responses,,3),
  unique_emails, UNIQUE(FILTER(emails, emails<>"")),
  
  results, MAP(unique_emails, LAMBDA(e,
    LET(
      hist_actions, FILTER(actions, emails=e),
      last_action, IF(COUNTA(hist_actions)=0, "", INDEX(hist_actions, ROWS(hist_actions))),
      IF(LOWER(last_action)="subscribe", e, "")
    )
  )),
  
  SORT(FILTER(results, results<>""))
)
````



## Required GitHub Secrets

Add the following secrets in:
GitHub → Repository Settings → Secrets and Variables → Actions

GMAIL_SENDER
Workspace Gmail address used to send the daily alerts

CREDENTIALS_JSON
Full Gmail OAuth client credentials JSON (pasted as a single line)

GOOGLE_SERVICE_ACCOUNT_JSON
Full Google Sheets service account JSON (pasted as a single line)

SHEET_ID
The Google Sheet ID containing the subscriber list



## .gitignore Requirements

The following must be ignored and not committed:

*.json
token.json
credentials.json
env/
downloads/
__pycache__/



Once GitHub Secrets and Google credentials are correctly configured by MCFN, the system becomes fully automated and requires no ongoing intervention.
