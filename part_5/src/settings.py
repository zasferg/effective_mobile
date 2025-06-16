from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.environ.get("TEST_DB_NAME")
DB_HOST = os.environ.get("TEST_DB_HOST")
DB_PORT = os.environ.get("TEST_DB_PORT")
DB_USER = os.environ.get("TEST_DB_USER")
DB_PASSWORD = os.environ.get("TEST_DB_PASSWORD")

REDIS_PORT = os.environ.get("REDIS_PORT")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(DATABASE_URL)