from datetime import datetime
from typing import Optional

from fastapi.exceptions import RequestValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core import configs
from core.password import hash_password
from crud.verification import create_otp_for_user, find_otp_by_code, delete_all_otp_by_user_id
from models.user import User, UserRole


async def get_role_by_alias(db: AsyncSession, alias: str):
    result = await db.execute(
        select(UserRole).filter(UserRole.alias == alias)
    )
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, phone_number: str, username:str, password: str, first_name: str, last_name: Optional[str]=None):
    try:
        async with db.begin():
            role = await get_role_by_alias(db, UserRole.CLIENT_ALIAS)

            new_user = User(
                role_id=role.id,
                phone_number=phone_number,
                username=username,
                password=hash_password(password),
                first_name=first_name,
                last_name=last_name,
            )

            db.add(new_user)
            await db.flush()

            await create_otp_for_user(db, new_user.id)

        await db.refresh(new_user)

        return new_user
    except IntegrityError:
        await db.rollback()
        raise RequestValidationError([{
            "loc": ("body", "phone_number"),
            "msg": "User with this phone number already exists",
            "type": "value_error.duplicate"
        }])


async def find_user_by_phone_number(db: AsyncSession, phone_number: str) -> User:
    result = await db.execute(
        select(User).where(User.phone_number == phone_number)
    )
    return result.scalar_one_or_none()


async def make_user_verified(db: AsyncSession, phone_number: str, otp: str) -> None:
    invalid_otp_error = RequestValidationError([{
        'loc': ['body', 'otp'],
        'msg': 'Invalid otp',
        'type': 'value_error.invalid_otp'
    }])
    expired_otp_error = RequestValidationError([{
        'loc': ['body', 'otp'],
        'msg': 'Otp has expired',
        'type': 'value_error.expired_otp'
    }])

    async with db.begin():
        user = await find_user_by_phone_number(db, phone_number)
        if not user:
            raise invalid_otp_error

        otp = await find_otp_by_code(db, user.id, otp)
        if not otp:
            raise invalid_otp_error

        otp_age = datetime.now() - otp.created_at
        if otp_age.seconds > configs.OTP_ALIVE_FOR_SECONDS:
            raise expired_otp_error

        user.is_verified = True
        await db.flush()

        await delete_all_otp_by_user_id(db, user.id)
