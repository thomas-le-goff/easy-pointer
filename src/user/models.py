import uuid

from sqlmodel import SQLModel, Field

class UserBase(SQLModel):
    login: str = Field(nullable=False, index=True)
    oauth2_provider: str = Field(nullable=False, index=True, default="github")
    oauth2_provider_user_id: str = Field(nullable=False, index=True)
    email: str | None = Field(nullable=True, default=None, index=True)
    avatar_url: str | None = Field(nullable=True, default=None)


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
