from functools import wraps

from flask import request

from HeroCode.models import Users


def login(f):
    @wraps(f)
    def wrap():
        body = request.json
        username = body.get('username', None)
        password = body.get('password', None)
        if None in [username, password]:
            return dict(status=False, reason='Missed data')
        else:
            user = Users.get(username=username)

            if user is None:
                return dict(status=False, reason='Wrong username')
            if user.password != password:
                return dict(status=False, reason='Wrong password')
            return f(user)

    return wrap