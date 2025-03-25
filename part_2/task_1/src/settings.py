
import os
from load_dotenv import load_dotenv

load_dotenv()

DB_NAME = os.environ.get("TEST_DB_NAME")
DB_HOST = os.environ.get("TEST_DB_HOST")
DB_PORT = os.environ.get("TEST_DB_PORT")
DB_USER = os.environ.get("TEST_DB_USER")
DB_PASSWORD = os.environ.get("TEST_DB_PASSWORD")

database_uri = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"