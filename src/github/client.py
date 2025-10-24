import httpx
import urllib.parse

from typing import Optional, Type
from types import TracebackType

from .config import GitHubSettingsDep
from .schemas import GitHubAccessToken, GitHubUserIn


class AsyncGitHubApiClient:
    def __init__(self, base_url, access_token: GitHubAccessToken) -> None:
        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers={
                "Accept": "application/json",
                "Authorization": access_token.as_http_header(),
            },
            timeout=10.0,
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> "AsyncGitHubApiClient":
        await self._client.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> Optional[bool]:
        return await self._client.__aexit__(exc_type, exc, tb)

    async def get_user(self) -> GitHubUserIn:
        r = await self._client.get("user")
        r.raise_for_status()
        return GitHubUserIn.model_validate(r.json())

# TODO: implements PKCE code challenge


class GitHubClient:

    def __init__(self, settings: GitHubSettingsDep) -> None:
        self.settings = settings

    def build_oauth2_authorize_uri(self, redirect_uri: str) -> str:
        query_params = {
            "client_id": self.settings.oauth2_client_id,
            "scope": " ".join(["read:user", "user:email"]),
            "redirect_uri": redirect_uri
        }

        return "{}/authorize?{}".format(
            self.settings.oauth2_base_uri,
            urllib.parse.urlencode(query_params)
        )

    async def request_access_token(self, code: str) -> GitHubAccessToken:
        async with httpx.AsyncClient() as client:
            headers = {
                "Accept": "application/json"
            }

            r = await client.post(
                "https://github.com/login/oauth/access_token", data={
                    "client_id": self.settings.oauth2_client_id,
                    "client_secret": self.settings.oauth2_client_secret,
                    "code": code,
                }, headers=headers)

            r.raise_for_status()

            return GitHubAccessToken.model_validate(r.json())

    def get_api_client(self, access_token: GitHubAccessToken) -> AsyncGitHubApiClient:
        return AsyncGitHubApiClient(self.settings.api_base_uri, access_token)
