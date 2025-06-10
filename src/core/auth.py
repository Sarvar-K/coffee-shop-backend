from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from core.jwt import create_access_token, create_refresh_token, decode_refresh_token
from crud.session import create_session, get_session_by_id
from crud.user import find_user_by_username
from exceptions import UnauthorizedError, ForbiddenError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(db: AsyncSession, username: str, password: str) -> dict:
    user = await find_user_by_username(db, username)
    if not user or not verify_password(password, user.password):
        raise UnauthorizedError('Invalid username or password')

    session = await create_session(db, user_id=user.id)
    session_id = session.id
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user, session_id)
    await db.commit()

    return dict(
        session_id=session_id,
        access_token=access_token,
        refresh_token=refresh_token,
    )


async def refresh_user_token(db: AsyncSession, refresh_token: str):
    token_data = decode_refresh_token(refresh_token)
    session = await get_session_by_id(db, session_id=token_data['sessionId'])
    if not session:
        raise ForbiddenError('Your authentication session does not exist, probably because your user was deleted')

    if session.is_terminated:
        raise ForbiddenError('Auth session has been terminated, please login again')

    return dict(
        session_id=session.id,
        access_token=create_access_token(session.user),
        refresh_token=create_refresh_token(session.user, session.id),
    )
