from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = "development"
    DATABASE_URL: str
    PORT: int = 8000

    class Config:
        env_file = ".env"

settings = Settings()

