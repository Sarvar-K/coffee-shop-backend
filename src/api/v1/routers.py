from fastapi import APIRouter

me_router = APIRouter(prefix='/me')
users_router = APIRouter(prefix='/users')
auth_router = APIRouter(prefix='/auth')