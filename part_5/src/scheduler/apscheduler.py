from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.cache.cache import redis_connection
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI

scheduler = AsyncIOScheduler()

async def delete_cache():
    await redis_connection.flushall()

async def lifespan(app: FastAPI):
    scheduler.add_job(
        func=delete_cache,
        trigger=CronTrigger(hour=14, minute=11),
        id="periodic_cache_clean",
        replace_existing=True,
    )

    scheduler.start()
    
    yield  
    
    scheduler.shutdown(wait=False)

