import redis.asyncio as redis
from src.settings import DB_HOST, REDIS_PORT

redis_connection = redis.Redis(
        host=DB_HOST,
        port=REDIS_PORT,
        decode_responses=True
        )

async def get_redis():
    try:
        yield redis_connection 
    finally:
        await redis_connection.close()
