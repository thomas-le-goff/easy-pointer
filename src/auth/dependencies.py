import jwt

from fastapi import Depends, status
from typing import Annotated
from jwt.exceptions import InvalidTokenError

from fastapi.exceptions import HTTPException

from .config import AuthSettingsDep
from .auth import AccessTokenBuilder, OAuth2AuthorizationCodeBearerWithCookie
from .schemas import TokenData

from ..user.dao import get_user_by_id
from ..user.models import User
from ..dependencies import SessionDep

oauth2_scheme = OAuth2AuthorizationCodeBearerWithCookie(
    tokenUrl="token",
    authorizationUrl="auth",
    cookie_name="app_session"
)


async def get_current_user(authSettings: AuthSettingsDep, token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, authSettings.secret_key,
                             algorithms=[authSettings.algorithm])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(id=user_id)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_by_id(session, id=token_data.id)
    if user is None:
        raise credentials_exception
    return user

CurrentUserDep = Annotated[User, Depends(get_current_user)]

AccessTokenBuilderDep = Annotated[AccessTokenBuilder, Depends(
    AccessTokenBuilder)]
