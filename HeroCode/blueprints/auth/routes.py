from itsdangerous import SignatureExpired, BadSignature
from sqlalchemy.exc import IntegrityError
from flask import request
import re

from HeroCode.blueprints.auth import auth
from HeroCode.models import Users
from HeroCode import db

from utils import token_serializer
from utils import mailing
from utils import strings


@auth.route('/register', methods=['POST'])
def register():
    username = request.form.get('username', None)
    email = request.form.get('email', None)
    password = request.form.get('password', None)

    if None in [username, email, password]:
        return dict(status=False, reason=strings.missed_data)

    user = Users(username=username, email=email, password=password)

    db.session.add(user)

    try:
        db.session.commit()
    except IntegrityError as e:
        try:
            # https://stackoverflow.com/questions/4666973/how-to-extract-the-substring-between-two-markers
            duplicate_key = re.search('\'users.(.+?)\'"', e.args[0]).group(1)
        except AttributeError:
            return dict(status=False, reason=strings.unexpected_duplicate_error)

        return dict(status=False, reason=f'Duplicate key - {duplicate_key}')

    mailing.email_verification(email)

    return dict(status=True)


@auth.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', None)
    password = request.form.get('password', None)

    if None in [username, password]:
        return dict(status=False, reason=strings.missed_data)

    user = Users.get(username=username, password=password)
    if user is None:
        return dict(status=False, reason=strings.wrong_credentials)

    return dict(status=True, user=user.serialize())


@auth.route('/confirm-email/<token>')
def confirm_email(token: str):
    try:
        email = token_serializer.decode_token(token, max_age=3600)
    except SignatureExpired:
        return dict(status=False, reason=strings.expired_token)
    except BadSignature:
        return dict(status=False, reason=strings.wrong_token)

    user = Users.get(email=email)
    user.is_active = 1
    db.session.commit()

    return dict(status=True)
