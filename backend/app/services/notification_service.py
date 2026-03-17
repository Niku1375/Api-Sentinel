# app/services/notification_service.py
import smtplib
from email.mime.text import MIMEText

from app.config import settings

def send_email_alert(to_email: str, subject: str, message: str):
    """
    Sends an email alert using SMTP settings from config.
    Can be used with test SMTP (Mailtrap) or real SMTP.
    """

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = to_email

    try:
        # Connect to SMTP server
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.starttls()  # enable TLS
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

        # Send the message
        server.send_message(msg)
        print(f"[Email sent] Subject: {subject} To: {to_email}")

    except Exception as e:
        # Print error but don't crash the worker
        print(f"[Email failed] Subject: {subject} To: {to_email} Error: {e}")

    finally:
        server.quit()