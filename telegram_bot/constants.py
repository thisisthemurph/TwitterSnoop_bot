import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN")

TW_API_KEY: str = os.getenv("TW_API_KEY")
TW_API_KEY_SECRET: str = os.getenv("TW_API_KEY_SECRET")
TW_BEARER_TOKEN: str = os.getenv("TW_BEARER_TOKEN")
TW_ACCESS_TOKEN: str = os.getenv("TW_ACCESS_TOKEN")
TW_ACCESS_TOKEN_SECRET: str = os.getenv("TW_ACCESS_TOKEN_SECRET")

API_BASE: str = os.getenv("DB_API_BASE", "http://localhost:5000")
