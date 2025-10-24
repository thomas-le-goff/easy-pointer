import uuid

from pydantic import BaseModel, Field, ConfigDict

class UserOut(BaseModel):
    id: uuid.UUID
    login: str
    email: str | None = None
    avatar_url: str | None = None