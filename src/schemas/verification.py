from pydantic import BaseModel, Field, field_validator


class VerifyPhoneNumberSchema(BaseModel):
    phone_number: str = Field(..., min_length=5, max_length=32)
    otp: str = Field(..., min_length=6, max_length=6)

    @field_validator('phone_number')
    @classmethod
    def phone_digits_only(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("Phone number must contain digits only")
        return v

    @field_validator('otp')
    @classmethod
    def otp_digits_only(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("Otp must contain digits only")
        return v
