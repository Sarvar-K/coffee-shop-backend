from typing import Annotated

from pydantic import BaseModel, field_validator, StringConstraints


def NonEmptyString(min_length=1, max_length=None):
    return Annotated[str, StringConstraints(strip_whitespace=True, min_length=min_length, max_length=max_length)]


class PhoneNumberSchema(BaseModel):
    phone_number: NonEmptyString(min_length=5, max_length=32)

    @field_validator('phone_number')
    @classmethod
    def phone_digits_only(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError('Phone number must contain digits only')

        return v
