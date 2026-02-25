from os import getenv

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = getenv("DATABASE_URL", None)
SECRET_KEY = getenv("SECRET_KEY", None)

ALGORITHM = getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRES_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRES_MINUTES", 15))
REFRESH_TOKEN_EXPIRES_MINUTES = int(getenv("REFRESH_TOKEN_EXPIRES_MINUTES", 7200))
ACCOUNT_PROCCESS_EXPIRES_MINUTES = int(getenv("ACCOUNT_PROCCESS_EXPIRES_MINUTES", 15))


if not DATABASE_URL:
    raise ValueError("No database url was found.")
elif not SECRET_KEY:
    raise ValueError("No secret key found.")
