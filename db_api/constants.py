import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST: str = os.getenv("DB_HOST")
DB_NAME: str = os.getenv("DB_NAME")
DB_USER: str = os.getenv("DB_USER")
DB_PASSWORD: str = os.getenv("DB_PASSWORD")

DB_API_HOST: str = os.getenv("DB_API_HOST") or "127.0.0.1"
DB_API_PORT: int = int(os.getenv("DB_API_PORT") or 5000)
