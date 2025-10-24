from fastapi import Depends
from typing import Annotated
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class GitHubSettings(BaseSettings):
    oauth2_client_id: str
    oauth2_client_secret: str
    oauth2_base_uri: str
    oauth2_access_token_uri: str
    api_base_uri: str

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="GITHUB_", extra="ignore")


@lru_cache
def get_github_settings():
    return GitHubSettings()  # type: ignore


GitHubSettingsDep = Annotated[GitHubSettings, Depends(get_github_settings)]
