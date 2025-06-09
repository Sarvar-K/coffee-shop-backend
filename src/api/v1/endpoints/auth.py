from fastapi import Depends, APIRouter, status
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import create_user, make_user_verified
from dependencies.db import get_db_session
from schemas.user import UserCreateRequestSchema, UserCreateResponseSchema
from schemas.verification import VerifyPhoneNumberSchema

auth_router = APIRouter(prefix='/auth')


@auth_router.post('/signup', response_model=UserCreateResponseSchema)
async def register_user(payload: UserCreateRequestSchema, db: AsyncSession = Depends(get_db_session)):
    return await create_user(
        db=db,
        phone_number=payload.phone_number,
        username=payload.username,
        password=payload.password,
        first_name=payload.first_name,
        last_name=payload.last_name
    )


@auth_router.post('/verify')
async def verify_phone_number(payload: VerifyPhoneNumberSchema, db: AsyncSession = Depends(get_db_session)):
    await make_user_verified(
        db=db,
        phone_number=payload.phone_number,
        otp=payload.otp,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
