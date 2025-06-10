from datetime import datetime
from typing import Optional

from fastapi.exceptions import RequestValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core import configs
from crud.helpers import find_unique_constraint_violator
from crud.verification import create_otp_for_user, find_otp_by_code, delete_all_otp_by_user_id
from models.user import User, UserRole


async def get_role_by_alias(db: AsyncSession, alias: str):
    result = await db.execute(
        select(UserRole).filter(UserRole.alias == alias)
    )
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, phone_number: str, username:str, hashed_password: str, first_name: str, last_name: Optional[str]=None):
    try:
        async with db.begin():
            role = await get_role_by_alias(db, UserRole.CLIENT_ALIAS)

            new_user = User(
                role_id=role.id,
                phone_number=phone_number,
                username=username,
                password=hashed_password,
                first_name=first_name,
                last_name=last_name,
            )

            db.add(new_user)
            await db.flush()

            await create_otp_for_user(db, new_user.id)

        await db.refresh(new_user)

        return new_user
    except IntegrityError as e:
        field_name = find_unique_constraint_violator(e)

        loc = field_name
        msg = f'User with this {field_name} already exists'
        if not field_name:
            loc = 'unknown_field'
            msg = 'Unique constraint violation, could not determine field name that causes duplication'

        raise RequestValidationError([{
            "loc": ('body', loc),
            "msg": msg,
            "type": 'value_error.duplicate'
        }])


async def find_user_by_phone_number(db: AsyncSession, phone_number: str) -> Optional[User]:
    result = await db.execute(
        _get_user_query().where(User.phone_number == phone_number)
    )
    return result.scalar_one_or_none()


async def find_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    result = await db.execute(
        _get_user_query().where(User.username == username)
    )
    return result.scalar_one_or_none()


async def find_user_by_id(db: AsyncSession, id: int):
    result = await db.execute(
        _get_user_query().where(User.id == id)
    )
    return result.scalar_one_or_none()


def _get_user_query():
    return select(User).options(joinedload(User.role, innerjoin=True))


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
