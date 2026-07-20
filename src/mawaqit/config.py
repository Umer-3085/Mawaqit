from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List

class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Mawaqit API"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: str = "development"

    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False

    database_url: str = Field(
        default="mysql+aiomysql://root:password@localhost:3306/mawaqit",
        description="Async MySQL connection string",
    )
    database_pool_size: int = 10
    database_max_overflow: int = 20
    database_echo: bool = False

    redis_url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection string",
    )

    secret_key: str = Field(
        default="CHANGE_ME_IN_PRODUCTION_MIN_32_CHARS",
        min_length=32,
        description="JWT secret key",
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        description="Allowed CORS origins",
    )

    quran_api_base_url: str = "https://api.alquran.cloud/v1"
    quran_api_timeout: float = 10.0

    default_calculation_method: str = "MOON_SIGHTING_COMMITTEE"
    default_madhab: str = "SHAFI"
    default_school: str = "STANDARD"

    log_level: str = "INFO"
    log_format: str = "json"

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()