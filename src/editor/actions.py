from fastapi import APIRouter, status, Response
from fastapi.responses import HTMLResponse

from .dependencies import CodeManagerDep
from .editor import EditorWriteIn, EditorReadIn

router = APIRouter(
    prefix="/editor",
    tags=["editor"]
)


@router.put("/code", response_class=Response, status_code=status.HTTP_204_NO_CONTENT)
async def put_code(body: EditorWriteIn, code_manager: CodeManagerDep):
    await code_manager.write(body)


@router.get("/code")
def get_code(code_manager: CodeManagerDep):
    return code_manager.read(EditorReadIn())


@router.get("/game", response_class=HTMLResponse)
async def get_game(code_manager: CodeManagerDep):
    return await code_manager.render()
