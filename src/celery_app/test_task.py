import asyncio

from .tasks import delete_unverified_users


async def test_task():
    result = await delete_unverified_users()
    print("Task result:", result)


if __name__ == "__main__":
    asyncio.run(test_task())
