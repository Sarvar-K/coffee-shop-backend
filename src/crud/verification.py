import random

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core import configs
from models.verification import Otp


async def create_otp_for_user(db: AsyncSession, user_id: int) -> Otp:
    for attempt in range(configs.MAX_OTP_GENERATION_ATTEMPTS):
        otp_code = f"{random.randint(100000, 999999)}"
        otp = Otp(
            user_id=user_id,
            code=otp_code,
        )
        db.add(otp)

        try:
            await db.flush()
            return otp
        except IntegrityError:
            await db.rollback()
            if attempt == configs.MAX_OTP_GENERATION_ATTEMPTS - 1:
                raise ValueError("Failed to generate a unique OTP after several attempts.")


async def find_otp_by_code(db: AsyncSession, user_id: int, code: str) -> Otp:
    query = select(Otp).where(Otp.user_id == user_id, Otp.code == code)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def delete_all_otp_by_user_id(db: AsyncSession, user_id: int):
    await db.execute(
        delete(Otp).where(Otp.user_id == user_id)
    )
    await db.flush()
