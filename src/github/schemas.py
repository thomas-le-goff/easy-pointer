from pydantic import BaseModel, Field, ConfigDict


from ..user.models import UserBase


class GitHubUserIn(UserBase):
    oauth2_provider_user_id: str = Field(validation_alias="id")

    model_config = ConfigDict(coerce_numbers_to_str=True)  # type: ignore


class GitHubAccessToken(BaseModel):
    access_token: str
    token_type: str
    scope: str

    def as_http_header(self):
        return f'{self.token_type} {self.access_token}'
