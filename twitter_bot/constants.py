import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN")

TW_API_KEY: str = os.getenv("TW_API_KEY")
TW_API_KEY_SECRET: str = os.getenv("TW_API_KEY_SECRET")
TW_BEARER_TOKEN: str = os.getenv("TW_BEARER_TOKEN")
TW_ACCESS_TOKEN: str = os.getenv("TW_ACCESS_TOKEN")
TW_ACCESS_TOKEN_SECRET: str = os.getenv("TW_ACCESS_TOKEN_SECRET")

TW_SLEEP_TIMEOUT_SECONDS: int = int(os.getenv("TW_SLEEP_TIMEOUT_SECONDS", default=None) or 60)
TW_MAX_FETCH_COUNT: int = int(os.getenv("TW_MAX_FETCH_COUNT", default=None) or 10)