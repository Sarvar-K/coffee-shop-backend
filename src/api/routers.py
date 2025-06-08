from fastapi import APIRouter

from api.v1 import routers

main_router = APIRouter(prefix='/v1')

main_router.include_router(routers.users_router)
main_router.include_router(routers.me_router)
main_router.include_router(routers.auth_router)