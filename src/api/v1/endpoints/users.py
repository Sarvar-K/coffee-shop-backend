from typing import List, Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud.session import delete_sessions_by_user_id
from crud.user import find_all_users, find_user_by_id, partially_update_user, exists_user_by_id, delete_user_by_id
from crud.verification import delete_all_otp_by_user_id
from dependencies.auth import get_current_active_admin
from dependencies.db import get_db_session
from exceptions import NotFoundError
from models.user import User
from schemas.user import UserWithAliasResponse, UserPatchRequestSchema

users_router = APIRouter(prefix='/users')


@users_router.get('', response_model=List[UserWithAliasResponse])
async def list_all_users(current_admin: Annotated[User, Depends(get_current_active_admin)], db: AsyncSession = Depends(get_db_session)):
    return await find_all_users(db)


@users_router.get('/{user_id}', response_model=UserWithAliasResponse)
async def find_user(
        user_id: int,
        current_admin: Annotated[User, Depends(get_current_active_admin)],
        db: AsyncSession = Depends(get_db_session)
):
    user = await find_user_by_id(db, user_id)
    if not user:
        raise NotFoundError('User not found')

    return user


@users_router.patch('/{user_id}', response_model=UserWithAliasResponse)
async def patch_user(
        user_id: int,
        update_schema: UserPatchRequestSchema,
        db: AsyncSession = Depends(get_db_session)
):
    user = await find_user_by_id(db, user_id)
    if not user:
        raise NotFoundError('User not found')

    await partially_update_user(db, user, update_schema.dict(exclude_unset=True))

    await db.commit()
    await db.refresh(user)
    return user


@users_router.delete('/{user_id}')
async def delete_user(
        user_id: int,
        db: AsyncSession = Depends(get_db_session)
):
    async with db.begin():
        user_exists = await exists_user_by_id(db, user_id)
        if not user_exists:
            raise NotFoundError('User not found')

        await delete_all_otp_by_user_id(db, user_id)
        await delete_sessions_by_user_id(db, user_id)
        await delete_user_by_id(db, user_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
