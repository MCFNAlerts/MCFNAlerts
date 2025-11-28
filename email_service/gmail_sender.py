import base64
from email.message import EmailMessage
from email_service.credentials_loader import get_gmail_service
from config import GMAIL_SENDER

def send_email(recipients, subject, html_body):
    service = get_gmail_service()

    message = EmailMessage()
    message["To"] = GMAIL_SENDER      # must have a "To"
    message["From"] = GMAIL_SENDER
    message["Subject"] = subject

    message["Bcc"] = ", ".join(recipients)

    message.set_content("This email requires HTML client support.")
    message.add_alternative(html_body, subtype="html")

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    send_body = {"raw": encoded_message}

    sent = service.users().messages().send(
        userId="me",
        body=send_body
    ).execute()

    return sent

def chunk_list(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]

