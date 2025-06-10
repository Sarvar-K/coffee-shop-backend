from pydantic import BaseModel

from core import configs
from schemas.shared import NonEmptyStringField, UsernameField, PasswordField


class TokenCreateRequestSchema(BaseModel):
    username: UsernameField
    password: PasswordField


class TokenRefreshRequestSchema(BaseModel):
    refresh_token: NonEmptyStringField()


class TokenResponseSchema(BaseModel):
    session_id: int
    access_token: str
    refresh_token: str
    access_expires_in: int = configs.ACCESS_TOKEN_ALIVE_FOR_MINUTES * 60
    refresh_expires_in: int = configs.REFRESH_TOKEN_ALIVE_FOR_MINUTES * 60
