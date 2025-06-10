from typing import Annotated

from fastapi import APIRouter, Depends

from dependencies.auth import get_current_active_user
from models.user import User
from schemas.user import UserWithAliasResponse

me_router = APIRouter(prefix='/me')

@me_router.get('', response_model=UserWithAliasResponse)
async def read_my_user(current_user_awaitable: Annotated[User, Depends(get_current_active_user)]):
    return current_user_awaitable
