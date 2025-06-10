import os


POSTGRES_DB = os.environ['POSTGRES_DB']
POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
DB_HOST = os.environ['DB_HOST']
POSTGRES_PORT = os.environ['POSTGRES_PORT']

DB_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

POSTGRES_SCHEMA = 'coffee_shop_backend'

CORS_SETTINGS = {
    'allow_origins': ['*'],
    'allow_credentials': True,
    'allow_methods': ['*'],
    'allow_headers': ['*'],
}

MAX_OTP_GENERATION_ATTEMPTS = 5
OTP_ALIVE_FOR_SECONDS = 120

ACCESS_TOKEN_ALIVE_FOR_MINUTES = 10
REFRESH_TOKEN_ALIVE_FOR_MINUTES = 24 * 60
