from fastapi import Depends, APIRouter, status
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import hash_password, authenticate_user, refresh_user_token
from crud.user import create_user, make_user_verified
from dependencies.db import get_db_session
from schemas.token import TokenResponseSchema, TokenCreateRequestSchema, TokenRefreshRequestSchema
from schemas.user import UserCreateRequestSchema, UserCreateResponseSchema
from schemas.verification import VerifyPhoneNumberSchema

auth_router = APIRouter(prefix='/auth')


@auth_router.post('/signup', response_model=UserCreateResponseSchema)
async def register_user(payload: UserCreateRequestSchema, db: AsyncSession = Depends(get_db_session)):
    return await create_user(
        db=db,
        phone_number=payload.phone_number,
        username=payload.username,
        hashed_password=hash_password(payload.password),
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


@auth_router.post('/login', response_model=TokenResponseSchema)
async def login(payload: TokenCreateRequestSchema, db: AsyncSession = Depends(get_db_session)):
    return TokenResponseSchema(**await authenticate_user(
        db,
        username=payload.username,
        password=payload.password,
    ))


@auth_router.post('/refresh', response_model=TokenResponseSchema)
async def login(payload: TokenRefreshRequestSchema, db: AsyncSession = Depends(get_db_session)):
    return TokenResponseSchema(**await refresh_user_token(
        db,
        refresh_token=payload.refresh_token,
    ))
