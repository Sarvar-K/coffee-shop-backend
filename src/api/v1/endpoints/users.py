from typing import List, Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import find_all_users, find_user_by_id
from dependencies.auth import get_current_active_admin
from dependencies.db import get_db_session
from exceptions import NotFoundError
from models.user import User
from schemas.user import UserWithAliasResponse

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
