from itsdangerous import URLSafeTimedSerializer
from email.message import EmailMessage
from smtplib import SMTP_SSL
from flask import url_for
from os import getenv


class Mailing:

    def __init__(self):
        self.secret_key = getenv('SECRET_KEY')
        self.sender = getenv('SMTP_SENDER')
        self.port = int(getenv('SMTP_PORT'))
        self.password = getenv('SMTP_PASSWORD')
        self.url_serializer = URLSafeTimedSerializer(self.secret_key)

    def __generate_token(self, value: str):
        token = self.url_serializer.dumps(value, salt=self.secret_key)
        return url_for('auth.register', token=token, _external=True)

    def email_verification(self, email: str):
        mail = EmailMessage()
        mail['subject'] = 'Email verification'
        mail['From'] = self.sender
        mail['To'] = email
        mail.set_content(self.__generate_token(email))

        with SMTP_SSL('smtp.gmail.com', self.port) as SMTP:
            SMTP.login(self.sender, self.password)
            SMTP.send_message(mail)
