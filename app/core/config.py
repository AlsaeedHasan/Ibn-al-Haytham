from os import getenv

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = getenv("DATABASE_URL", None)

if not DATABASE_URL:
    raise ValueError("No database url was found.")
