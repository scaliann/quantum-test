from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    API_URL: str = "http://api:8000"

    class Config:
        env_file = ".env"


settings = Settings()
