from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    API_URL: str = "http://api:8000"

    class Config:
        env_file = ".env"


settings = Settings()
