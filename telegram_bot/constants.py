import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN")

TW_API_KEY: str = os.getenv("TW_API_KEY")
TW_API_KEY_SECRET: str = os.getenv("TW_API_KEY_SECRET")
TW_BEARER_TOKEN: str = os.getenv("TW_BEARER_TOKEN")
TW_ACCESS_TOKEN: str = os.getenv("TW_ACCESS_TOKEN")
TW_ACCESS_TOKEN_SECRET: str = os.getenv("TW_ACCESS_TOKEN_SECRET")

DB_API_HOST: str = os.getenv("DB_API_HOST") or "127.0.0.1"
DB_API_PORT: int = int(os.getenv("DB_API_PORT") or 5000)
