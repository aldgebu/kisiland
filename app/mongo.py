from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.settings import settings


db = None

client: Optional[AsyncIOMotorClient] = None


async def connect_to_mongo_db():
    global db, client
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client[settings.MONGODB_DATABASE]


async def disconnect_to_mongo_db():
    global client
    client.close()


def get_mongo_db() -> Optional[AsyncIOMotorDatabase]:
    return db
