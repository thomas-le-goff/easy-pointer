import jwt

from datetime import datetime, timedelta, timezone

from fastapi import Request, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.security.utils import get_authorization_scheme_param

from .schemas import Token
from .config import AuthSettingsDep


class AccessTokenBuilder():

    def __init__(self, settings: AuthSettingsDep) -> None:
        self.settings = settings

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> Token:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, self.settings.secret_key, algorithm=self.settings.algorithm)
        return Token(value=encoded_jwt, token_type="Bearer")


class OAuth2AuthorizationCodeBearerWithCookie(OAuth2AuthorizationCodeBearer):

    def __init__(
        self,
        *args,
        cookie_name: str = "app_session",
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.cookie_name = cookie_name

    async def __call__(self, request: Request) -> str | None:
        authorization = request.headers.get("Authorization") or ""
        scheme, param = get_authorization_scheme_param(authorization)

        if authorization and scheme.lower() == "bearer":
            return param

        authorization = request.cookies.get(self.cookie_name)

        if authorization:
            return authorization

        if self.auto_error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return None
