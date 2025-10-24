from fastapi import APIRouter, Request, status

from fastapi.responses import RedirectResponse, Response

from .dependencies import SessionDep, AccessTokenBuilderDep

from ..github.dependencies import GitHubClientDep
from ..user.dao import get_user_by_oauth2_provider_user_id
from ..user.models import User

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/logout")
def post_logout(request: Request, response_class=Response):
    response = Response(status_code=status.HTTP_205_RESET_CONTENT)
    response.delete_cookie(
        key="app_session",
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
    )
    return response


@router.get("/github/authorize", response_class=RedirectResponse)
def get_github_auth(request: Request, github_client: GitHubClientDep):
    return RedirectResponse(
        github_client.build_oauth2_authorize_uri(
            str(request.url_for('github_redirect')))
    )


@router.get("/github/redirect", response_class=RedirectResponse)
async def github_redirect(code: str, request: Request, session: SessionDep, accessTokenBuilder: AccessTokenBuilderDep, github_client: GitHubClientDep):
    access_token = await github_client.request_access_token(code)

    async with github_client.get_api_client(access_token) as api_client:
        github_user = await api_client.get_user()

        existing_user = get_user_by_oauth2_provider_user_id(
            session, github_user.oauth2_provider_user_id)

        # Upsert user
        if existing_user != None:
            existing_user.sqlmodel_update(
                github_user.model_dump(exclude_unset=True))
        else:
            existing_user = User.model_validate(github_user)
        session.add(existing_user)
        session.commit()
        session.refresh(existing_user)

        # TODO: add refresh token

        access_token = accessTokenBuilder.create_access_token(
            data={"sub": str(existing_user.id)})

        resp = RedirectResponse(
            "/auth/success",
            headers={"Authorization": access_token.as_authorization_header()},
            status_code=status.HTTP_303_SEE_OTHER
        )

        resp.set_cookie(
            key="app_session",
            value=access_token.value,
            httponly=True,
            secure=True,
            samesite="lax",
            path="/",
            max_age=1800,  # TODO: add domain
        )

        return resp
