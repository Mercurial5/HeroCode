from dotenv import load_dotenv
from os import getenv

from urllib.parse import quote_plus


load_dotenv()

user = getenv('DATABASE_USER')
password = getenv('DATABASE_PASSWORD')
host = getenv('DATABASE_HOST')
name = getenv('DATABASE_NAME')
port = getenv('DATABASE_PORT')
db_type = getenv('DATABASE_TYPE')
params = getenv('DATABASE_PARAMS')


class Config:
    SQLALCHEMY_DATABASE_URI = f'{db_type}://{user}:{quote_plus(password)}@{host}/{name}{params}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = getenv('SECRET_KEY')
