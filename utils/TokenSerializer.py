from itsdangerous import URLSafeTimedSerializer
from os import getenv


class TokenSerializer:

    def __init__(self):
        self.url_serializer = URLSafeTimedSerializer(getenv('SECRET_KEY'))

    def generate_token(self, value: str) -> str:
        return self.url_serializer.dumps(value, salt=getenv('SECRET_KEY'))

    def decode_token(self, token: str, max_age: int):
        return self.url_serializer.loads(token, salt=getenv('SECRET_KEY'), max_age=max_age)
