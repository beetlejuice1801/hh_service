from pydantic import BaseModel, SecretStr


class CodeResponse(BaseModel):
    access_token: SecretStr = str
    expires_in: int
    refresh_token: SecretStr = str
    token_type: str = "bearer"



