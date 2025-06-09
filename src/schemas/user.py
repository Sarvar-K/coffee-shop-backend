from datetime import datetime
from typing import Optional

from pydantic import Field

from schemas.shared import PhoneNumberSchema, NonEmptyString


class UserBaseSchema(PhoneNumberSchema):
    username: NonEmptyString(min_length=6, max_length=128)
    first_name: NonEmptyString(min_length=1, max_length=128)
    last_name: Optional[str] = Field(None, max_length=128)


class UserCreateRequestSchema(UserBaseSchema):
    password: NonEmptyString(min_length=8, max_length=128)


class UserCreateResponseSchema(UserBaseSchema):
    id: int
    created_at: datetime
    edited_at: datetime
    is_verified: bool
    is_active: bool

    class Config:
        from_attributes = True
