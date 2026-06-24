from functools import lru_cache
from pydantic_settings import BaseSettings,SettingsConfigDict


class Settings(BaseSettings):

    app_name:str ="Threat Intelligence Platform"
    app_version:str="0.1.0"


    database_url:str="sqlite:///./threat.db"

    log_level:str="INFO"

    AI_PROVIDER: str = "gemini"

    GEMINI_API_KEY: str | None = None

    GEMINI_MODEL: str = (
    "gemini-2.5-flash"
)

    model_config=SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )

@lru_cache
def get_settings()->Settings:
    
    return Settings()

settings=get_settings()