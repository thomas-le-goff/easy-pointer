from fastapi import Depends
from typing import Annotated

from fastapi.exceptions import HTTPException

from ..editor.config import EditorSettingsDep
from ..editor.editor import CodeManager
from ..auth.dependencies import CurrentUserDep


def get_current_user_code_manager(editorSettings: EditorSettingsDep, current_user: CurrentUserDep):
    return CodeManager(editorSettings, current_user, "hello-world")


CodeManagerDep = Annotated[CodeManager, Depends(get_current_user_code_manager)]
