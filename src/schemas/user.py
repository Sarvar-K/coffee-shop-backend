from typing import Optional

from pydantic import BaseModel, Field, field_validator


class UserCreateSchema(BaseModel):
    phone_number: str = Field(..., min_length=5, max_length=32)
    first_name: str = Field(..., min_length=1, max_length=128)
    last_name: Optional[str] = Field(None, max_length=128)
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator('phone_number')
    @classmethod
    def digits_only(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("Phone number must contain digits only")
        return v
