from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.jwt import decode_access_token
from crud.user import find_user_by_id
from dependencies.db import get_db_session
from exceptions import ServerError, ForbiddenError
from models.user import User, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/v1/auth/login')


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(get_db_session)):
    payload = decode_access_token(token)
    user_id = payload['sub']

    user = await find_user_by_id(db, int(user_id))
    if user is None:
        raise ServerError(f'Access token did not produce user, user_id={user_id}')

    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if not current_user.is_active:
        raise ForbiddenError('Your account has been deactivated')

    return current_user


async def get_current_active_admin(current_admin: Annotated[User, Depends(get_current_active_user)]):
    if not current_admin.role.alias == UserRole.ADMIN_ALIAS:
        raise ForbiddenError('This action is for admin users only')

    return current_admin
