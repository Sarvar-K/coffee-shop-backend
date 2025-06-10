from datetime import datetime
from typing import Optional

from pydantic import Field

from schemas.shared import PhoneNumberSchema, NonEmptyStringField, UsernameField, PasswordField


class UserBaseSchema(PhoneNumberSchema):
    username: UsernameField
    first_name: NonEmptyStringField(min_length=1, max_length=128)
    last_name: Optional[str] = Field(None, max_length=128)


class UserCreateRequestSchema(UserBaseSchema):
    password: PasswordField


class UserCreateResponseSchema(UserBaseSchema):
    id: int
    created_at: datetime
    edited_at: datetime
    is_verified: bool
    is_active: bool

    class Config:
        from_attributes = True
