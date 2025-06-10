from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models.session import Session
from models.user import User


async def create_session(db: AsyncSession, user_id: int):
    session = Session(
        user_id=user_id,
    )

    db.add(session)
    await db.flush()

    return session


async def get_session_by_id(db: AsyncSession, session_id: int):
    result = await db.execute(
        select(Session)
        .options(joinedload(Session.user, innerjoin=True).joinedload(User.role, innerjoin=True))
        .where(Session.id == session_id)
    )
    return result.scalar_one_or_none()
