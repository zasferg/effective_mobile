from dotenv import load_dotenv
import os
from pathlib import Path
load_dotenv()

URL = os.environ.get("URL")
STOP_YEAR = os.environ.get("STOP_YEAR")

DB_NAME = os.environ.get("TEST_DB_NAME")
DB_HOST = os.environ.get("TEST_DB_HOST")
DB_PORT = os.environ.get("TEST_DB_PORT")
DB_USER = os.environ.get("TEST_DB_USER")
DB_PASSWORD = os.environ.get("TEST_DB_PASSWORD")

database_uri = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
data_path=Path("/home/dmitry/Projects/effective_mobile/part_2/task_2/src/data")
