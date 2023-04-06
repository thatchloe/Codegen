import smtplib
from email.mime.text import MIMEText
import uuid
from django.conf import settings


def SendResetLink(subject, message, receiver_email):
    try:
        # sender email with 2 step verification enable
        sender_email = settings.SENDER_EMAIL
        # app password and also enable less secure. (while generating app password select app as "mail".)
        password = settings.APPPASSWORD
        msg = MIMEText(f'{message}')
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(e)
        return False


def generateToken():
    return str(uuid.uuid4()).replace('-', '')[:-3]+str(uuid.uuid4())[0:10]