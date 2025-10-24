from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from ..auth.dependencies import CurrentUserDep
from .schemas import UserOut

router = APIRouter(
    prefix="/users",
    tags=["user"]
)


@router.get("/me", response_model=UserOut)
async def read_users_me(
    current_user: CurrentUserDep,
):
    return jsonable_encoder(current_user)
