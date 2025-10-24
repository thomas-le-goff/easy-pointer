from fastapi import Depends
from typing import Annotated
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: str

    model_config = SettingsConfigDict(env_file=".env", env_prefix="AUTH_", extra="ignore")


@lru_cache
def get_auth_settings():
    return AuthSettings()  # type: ignore


AuthSettingsDep = Annotated[AuthSettings, Depends(get_auth_settings)]
