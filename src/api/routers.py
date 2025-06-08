from fastapi import APIRouter

from api.v1.endpoints.auth import auth_router
from api.v1.endpoints.me import me_router
from api.v1.endpoints.users import users_router

main_router = APIRouter(prefix='/v1')

main_router.include_router(users_router)
main_router.include_router(me_router)
main_router.include_router(auth_router)