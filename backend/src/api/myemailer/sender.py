import os
import smtplib
from email.message import EmailMessage

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 465))

def send_email(subject: str = "No subject provided", content: str = "No message provided", to_email: str = EMAIL_ADDRESS, from_email: str = EMAIL_ADDRESS) -> None:
    """
    Send an email using the configured SMTP settings.
    
    :param subject: Subject of the email
    :param content: Content of the email
    :param to_email: Recipient's email address
    :param from_email: Sender's email address (default is EMAIL_ADDRESS)
    """
    msg = EmailMessage()
    msg.set_content(content)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        return smtp.send_message(msg)
        

    
