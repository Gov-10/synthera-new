from celery_app import celery
import aiosmtplib
from email.message import EmailMessage
import os
import asyncio

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
async def async_send_email(to_email, subject, body):
    message = EmailMessage()
    message["From"] = SMTP_USER
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(
        message,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        username=SMTP_USER,
        password=SMTP_PASS,
        start_tls=True,
    )

@celery.task
def send_email(to_email: str, subject: str, body: str):
    asyncio.run(async_send_email(to_email, subject, body))
    return True
