import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV", "development")
PORT = int(os.getenv("PORT", 8000))
DATABASE_URL = os.getenv("DATABASE_URL")

