from fastapi import APIRouter

from api.v1.endpoints.auth import auth_router
from api.v1.endpoints.me import me_router
from api.v1.endpoints.users import users_router

PUBLIC_API_PREFIX = '/public'
USER_API_PREFIX = '/user'
ADMIN_API_PREFIX = '/admin'

main_router = APIRouter(prefix='/v1')

main_router.include_router(auth_router, prefix=PUBLIC_API_PREFIX)

main_router.include_router(me_router, prefix=USER_API_PREFIX)

main_router.include_router(users_router, prefix=ADMIN_API_PREFIX)