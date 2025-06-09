from typing import Optional

from pydantic import Field, field_validator

from schemas.shared import PhoneNumberSchema


class UserCreateSchema(PhoneNumberSchema):
    first_name: str = Field(..., min_length=1, max_length=128)
    last_name: Optional[str] = Field(None, max_length=128)
    password: str = Field(..., min_length=8, max_length=128)
