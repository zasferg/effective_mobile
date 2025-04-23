from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from src.models import Base
from src.settings import database_uri


# engine = create_engine(url=database_uri)
# Session = sessionmaker(bind=engine)
# session = Session()
async_engine = create_async_engine(url=database_uri)
async_session = async_sessionmaker(bind=async_engine,expire_on_commit=False, autoflush=False, )



