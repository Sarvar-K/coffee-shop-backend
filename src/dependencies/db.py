from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from db.session import DatabaseSessionManager
from core import configs

db_manager = DatabaseSessionManager(configs.DB_URL, configs.DB_URL)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with db_manager.session() as session:
        yield session
