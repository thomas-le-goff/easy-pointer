from typing import Annotated, ClassVar
from pydantic import BaseModel


class EditorWriteIn(BaseModel):
    code: str
    file_name: Annotated[str, ClassVar] = "src/main.c"


class EditorWriteOut(BaseModel):
    code: str
    file_name: Annotated[str, ClassVar] = "src/main.c"
    error: str | None = None


class EditorReadIn(BaseModel):
    file_name: Annotated[str, ClassVar] = "src/main.c"


class EditorReadOut(BaseModel):
    code: str
    file_name: Annotated[str, ClassVar] = "src/main.c"
    error: str | None = None
