from datetime import datetime, timedelta
from celery import Celery
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError

from celery.schedules import crontab
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from core import configs
from models.session import Session
from models.user import User
from models.verification import Otp

celery_app = Celery(
    'tasks',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/1',
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

engine = create_async_engine(configs.DB_URL, echo=False)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@celery_app.task(name='tasks.delete_unverified_users')
async def delete_unverified_users():
    session = AsyncSessionLocal()
    try:
        async with session.begin():
            cutoff_date = datetime.now() - timedelta(hours=configs.CELERY_CLEANUP_INTERVAL_HOURS)

            query = select(User.id).where(
                User.is_verified == False,
                User.created_at < cutoff_date
            )
            result = await session.execute(query)
            unverified_user_ids = [row[0] for row in result]

            if not unverified_user_ids:
                return {"status": "success", "message": "No unverified users to delete"}

            await session.execute(
                delete(Otp).where(Otp.user_id.in_(unverified_user_ids)))

            await session.execute(
                delete(Session).where(Session.user_id.in_(unverified_user_ids)))

            await session.execute(
                delete(User).where(User.id.in_(unverified_user_ids)))

            return {
                "status": "success",
                "message": f"Deleted {len(unverified_user_ids)} unverified users and their related data"
            }
    except SQLAlchemyError as e:
        return {
            "status": "error",
            "message": f"Database error: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}"
        }
    finally:
        await session.close()


celery_app.conf.beat_schedule = {
    # Executes every day at specified hour
    'delete-unverified-users-daily': {
        'task': 'tasks.delete_unverified_users',
        'schedule': crontab(hour=configs.CELERY_CLEANUP_START_AT_HOUR, minute=0),
    },
}
