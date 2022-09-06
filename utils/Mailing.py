from email.message import EmailMessage
from smtplib import SMTP_SSL
from flask import url_for
from os import getenv

from utils import token_serializer


class Mailing:

    def __init__(self):
        self.sender = getenv('SMTP_SENDER')
        self.port = int(getenv('SMTP_PORT'))
        self.password = getenv('SMTP_PASSWORD')

    def email_verification(self, email: str):
        mail = EmailMessage()
        mail['subject'] = 'Email verification'
        mail['From'] = self.sender
        mail['To'] = email

        token = token_serializer.generate_token(email)
        token = url_for('auth.confirm_email', token=token, _external=True)
        mail.set_content(token)

        with SMTP_SSL('smtp.gmail.com', self.port) as SMTP:
            SMTP.login(self.sender, self.password)
            SMTP.send_message(mail)
