from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.settings import DATABASE_URL
from typing import Generator

engine = create_async_engine(url=DATABASE_URL, echo=True)
async_session = async_sessionmaker(bind=engine, autocommit= False, autoflush=False,class_=AsyncSession)

async def get_session() -> Generator:
    session: AsyncSession  = async_session()
    try:
        yield session
    finally:
        await session.close()
        
