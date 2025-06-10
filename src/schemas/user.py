from datetime import datetime
from pydantic import Field, BaseModel

from schemas.shared import PhoneNumberSchema, NonEmptyStringField, UsernameField, PasswordField


class UserBaseSchema(PhoneNumberSchema):
    username: UsernameField
    first_name: NonEmptyStringField(min_length=1, max_length=128)
    last_name: NonEmptyStringField(max_length=128) = Field(None)


class UserPatchRequestSchema(BaseModel):
    first_name: NonEmptyStringField(min_length=1, max_length=128) = Field(None)
    last_name: NonEmptyStringField(max_length=128) = Field(None)


class UserCreateRequestSchema(UserBaseSchema):
    password: PasswordField


class UserResponseSchema(UserBaseSchema):
    id: int
    created_at: datetime
    edited_at: datetime
    is_verified: bool
    is_active: bool

    class Config:
        from_attributes = True


class UserWithAliasResponse(UserResponseSchema):
    role_alias: str = Field(..., serialization_alias='role')

    class Config:
        from_attributes = True
