# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    GEMINI_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()