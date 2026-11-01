from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class _Env(BaseSettings):
    DEBUG: bool = False
    SECRET_KEY: str
    ALLOWED_HOSTS: list[str] = []
    LANGUAGE_CODE: str = "en-US"
    TIMEZONE: str = "UTC"

    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int = 5432

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_env() -> _Env:
    return _Env()  # type: ignore


env = get_env()
