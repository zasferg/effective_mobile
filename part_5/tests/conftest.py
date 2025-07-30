import asyncio
import pytest, pytest_asyncio
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.models.models import *
from src.schemas.trade import SpimexTradeResultCreate
from src.cache.cache import redis_connection
from datetime import datetime, timedelta

fixture_data = [
  {
    "id": 17731,
    "exchange_product_id": "DST5VLD001O",
    "exchange_product_name": "ДТ ЕВРО, летнее, сорта C, эк. класса К5 марки ДТ-Л-К5 по ГОСТ 32511-2013, ЛПДС Володарская (франко-резервуар ОТП Транснефть)",
    "oil_id": "DST5",
    "delivery_basis_name": "ЛПДС Володарская",
    "delivery_basis_id": "VLD",
    "delivery_type_id": "O",
    "volume": 124,
    "total": 7509200,
    "count": 2,
    "date": (datetime.now().date() - timedelta(days=0)).strftime("%d.%m.%Y")
  },
  {
    "id": 1952,
    "exchange_product_id": "A692LUL060J",
    "exchange_product_name": "Бензин (АИ-92-К5) (ГОСТ 32513-2013/ГОСТ 32513-2023), Волгоград-группа станций (ст. отправления ОТП)",
    "oil_id": "A692",
    "delivery_basis_name": "Волгоград-группа станций",
    "delivery_basis_id": "LUL",
    "delivery_type_id": "J",
    "volume": 660,
    "total": 44231640,
    "count": 11,
    "date": (datetime.now().date() - timedelta(days=0)).strftime("%d.%m.%Y")
  },
  {
    "id": 28040,
    "exchange_product_id": "PPBAASR005A",
    "exchange_product_name": "Газы углеводородные сжиженные марка ПБА, Астрахань БП (самовывоз автотранспортом)",
    "oil_id": "PPBA",
    "delivery_basis_name": "Астрахань БП",
    "delivery_basis_id": "ASR",
    "delivery_type_id": "A",
    "volume": 25,
    "total": 650000,
    "count": 1,
    "date": (datetime.now().date() - timedelta(days=1)).strftime("%d.%m.%Y")
  },
  {
    "id": 1165,
    "exchange_product_id": "A692BSA005A",
    "exchange_product_name": "Бензин (АИ-92-К5) ГОСТ 32513-2013/ГОСТ 32513-2023, Балашовская НБ (самовывоз автотранспортом)",
    "oil_id": "A692",
    "delivery_basis_name": "Балашовская НБ",
    "delivery_basis_id": "BSA",
    "delivery_type_id": "A",
    "volume": 25,
    "total": 1695000,
    "count": 1,
    "date": (datetime.now().date() - timedelta(days=1)).strftime("%d.%m.%Y")
  },
  {
    "id": 16158,
    "exchange_product_id": "DSC5STI065F",
    "exchange_product_name": "ДТ ЕВРО сорт C (ДТ-Л-К5) минус 5, ст. Стенькино II (ст. отправления)",
    "oil_id": "DSC5",
    "delivery_basis_name": "ст. Стенькино II",
    "delivery_basis_id": "STI",
    "delivery_type_id": "F",
    "volume": 1170,
    "total": 68201900,
    "count": 15,
    "date": (datetime.now().date() - timedelta(days=2)).strftime("%d.%m.%Y")
  },
  {
    "id": 28143,
    "exchange_product_id": "PPBAOSU005A",
    "exchange_product_name": "Газы углеводородные сжиженные марка ПБА, УН ОСК (самовывоз автотранспортом)",
    "oil_id": "PPBA",
    "delivery_basis_name": "УН ОСК",
    "delivery_basis_id": "OSU",
    "delivery_type_id": "A",
    "volume": 50,
    "total": 1228000,
    "count": 4,
    "date": (datetime.now().date() - timedelta(days=2)).strftime("%d.%m.%Y")
  },
  {
    "id": 17608,
    "exchange_product_id": "DST5NVL001O",
    "exchange_product_name": "ДТ ЕВРО, летнее, сорта C, эк. класса К5 марки ДТ-Л-К5 по ГОСТ 32511-2013, ЛПДС Невская (франко-резервуар ОТП Транснефть)",
    "oil_id": "DST5",
    "delivery_basis_name": "ЛПДС Невская",
    "delivery_basis_id": "NVL",
    "delivery_type_id": "O",
    "volume": 371,
    "total": 22805620,
    "count": 5,
    "date": (datetime.now().date() - timedelta(days=3)).strftime("%d.%m.%Y")
  }
]

import settings

engine = create_async_engine(
      url=settings.DATABASE_URL,
      pool_pre_ping=True
  )

async_session = async_sessionmaker(bind=engine, autocommit= False, autoflush=False,class_=AsyncSession)

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def test_lock():
    return asyncio.Lock()

@pytest_asyncio.fixture(scope="session")
async def get_fixture_data():
    return [SpimexTradeResultCreate.model_validate(item).model_dump() for item in fixture_data] 

@pytest_asyncio.fixture(autouse=True, scope="session")
async def create_db_tables(get_fixture_data):
  
  await redis_connection.flushall()

  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.drop_all)
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)

  data = get_fixture_data
  async with async_session() as session:
        await session.execute(insert(SpimexTradingResulsts).values(data))
        await session.commit()
 


