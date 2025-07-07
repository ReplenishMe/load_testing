import os
import logging
import shutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_mail():
    try:
        directory = os.getenv('REPORT')
        sender_email = os.getenv('sender_email')
        receiver_email = os.getenv('receiver_email')
        password = os.getenv('mail_password')
        subject = os.getenv('subject')
        body = os.getenv('body')

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        if os.path.exists(directory) and os.path.isdir(directory):
            for root, dirs, files in os.walk(directory):
                for name in files:
                    with open(f"report/{name}", 'rb') as f:
                        attach = MIMEApplication(f.read(), _subtype="csv")
                        attach.add_header(
                            'Content-Disposition', 'attachment',
                            filename=name
                            )
                        msg.attach(attach)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        logger.info(f"report sender's email :{sender_email}")
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        logger.info("Email sent successfully!")

        if os.path.exists(directory) and os.path.isdir(directory):
            shutil.rmtree(directory)
    except Exception as e:
        logger.error(e)

        