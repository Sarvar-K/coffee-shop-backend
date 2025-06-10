from typing import Annotated

from pydantic import BaseModel, field_validator, StringConstraints


def NonEmptyStringField(min_length=1, max_length=None):
    return Annotated[str, StringConstraints(strip_whitespace=True, min_length=min_length, max_length=max_length)]


UsernameField = NonEmptyStringField(min_length=6, max_length=128)
PasswordField = NonEmptyStringField(min_length=8, max_length=128)


class PhoneNumberSchema(BaseModel):
    phone_number: NonEmptyStringField(min_length=5, max_length=32)

    @field_validator('phone_number')
    @classmethod
    def phone_digits_only(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError('Phone number must contain digits only')

        return v
