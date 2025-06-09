from pydantic import BaseModel, Field, field_validator


class PhoneNumberSchema(BaseModel):
    phone_number: str = Field(..., min_length=5, max_length=32)

    @field_validator('phone_number')
    @classmethod
    def phone_digits_only(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("Phone number must contain digits only")
        return v
