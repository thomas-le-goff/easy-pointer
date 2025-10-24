from fastapi import Depends
from typing import Annotated
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import FilePath, DirectoryPath
from pathlib import Path


class EditorSettings(BaseSettings):
    work_storage_path: Path = Path("/tmp/w4")
    template_path: DirectoryPath = Path("templates/w4")
    wasmfour_executable: FilePath

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="EDITOR_", extra="ignore")


@lru_cache
def get_editor_settings():
    return EditorSettings()  # type: ignore


EditorSettingsDep = Annotated[EditorSettings, Depends(get_editor_settings)]
