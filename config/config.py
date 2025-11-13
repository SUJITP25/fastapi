from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

ENV_PATH = Path(r"D:/desktop/agenticai/fastapi/campusx/.env")


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM:str
    model_config = SettingsConfigDict(env_file=ENV_PATH, extra="ignore")


Config = Settings()
