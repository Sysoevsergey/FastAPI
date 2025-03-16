import os
from dotenv import load_dotenv

load_dotenv("../.env_dev", verbose=True)

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
SQL_DEBUG = os.getenv("SQL_DEBUG", "True").lower() in ("true", "1")
PG_DSN = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

API_URL = os.getenv("API_URL")
