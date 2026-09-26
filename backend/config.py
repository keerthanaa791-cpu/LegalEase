from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "LegalEase"
    environment: str = "development"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.8-flash"
    frontend_origin: str = "http://localhost:8501"
    max_terms: int = 30
    max_text_length: int = 50000

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    return Settings()
