import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env.* file

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "TaskTrackr")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")

settings = Settings()