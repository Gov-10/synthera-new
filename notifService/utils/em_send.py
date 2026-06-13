import os
from dotenv import load_dotenv
load_dotenv()
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("notif")
sender_email = os.getenv("MY_EMAIL")
app_password = os.getenv("APP_PASSWORD")

def email_send(email, pres):
    if not sender_email or not app_password:
        logger.error(json.dumps({"event": "env_missing"}))
        raise ValueError("creds missing in env")
    if not email:
        raise ValueError("email address missing")
    subject= "Here is your file report"
    body= f"""
        Hi, thanks for using synthera.
        You can download your file report by clicking on the link below:
        {pres}
        Please note that the link will be active only for one hour
        """
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    server=None
    try:
        server= smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, email, msg.as_string())
        return True
    except Exception as e:
        raise e
    finally:
        if server:
            try:
                server.quit()
            except Exception:
                pass
    
    

    
    
