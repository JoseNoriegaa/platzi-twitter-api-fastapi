import os
import environ

_env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, 'secret-key'),
    PORT=(int, 8000),
    USES_DOCKER=(str, 'No'),
)

if _env('USES_DOCKER') != 'Yes':
    environ.Env.read_env()

# Variables
DEBUG = _env('DEBUG')
SECRET_KEY = _env('SECRET_KEY')
PORT = _env('PORT')

# Database
DATABASE_URL = _env('DATABASE_URL')
DATABASE_CONFIG = _env.db()

USERS_FILE = 'users.json'
USERS_STORAGE = os.path.join(os.path.dirname(__file__), '..', USERS_FILE)

TWEETS_FILE = 'tweets.json'
TWEETS_STORAGE = os.path.join(os.path.dirname(__file__), '..', TWEETS_FILE)
