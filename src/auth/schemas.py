from pydantic import BaseModel

class Token(BaseModel):
    value: str
    token_type: str

    def as_authorization_header(self) -> str:
        return f'{self.token_type} {self.value}'


class TokenData(BaseModel):
    id: str | None = None
