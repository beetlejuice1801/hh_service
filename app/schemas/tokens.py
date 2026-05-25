from pydantic import BaseModel, SecretStr


class CodeResponse(BaseModel):
    """Схема ответа с токенами от HH API."""

    access_token: SecretStr = str
    expires_in: int
    refresh_token: SecretStr = str
    token_type: str = "bearer"
