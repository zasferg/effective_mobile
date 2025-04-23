import asyncio
from src.utils.xml import group_to_list_generator
import os
from src.utils.loader import SqlAlchemySpimexTradingResulstsRepository
from src.models import SpimexTradingResulsts
from src.database import async_session
import pandas as pd
from src.settings import URL, STOP_YEAR
from src.parser.parser import parser
from src.settings import data_path


filename_list = os.listdir(data_path)
data_loader = SqlAlchemySpimexTradingResulstsRepository(session=async_session,model=SpimexTradingResulsts)

async def load_data(func):
        while True:
            try:
                data_row = await func.__anext__()
                if not any(pd.isna(item) for item in data_row):
                    await data_loader.load(data=data_row)
            except StopAsyncIteration:
                break

async def load_data_to_database(data_path: str,fname_list: list ):
    tasks = set()
    for fname in fname_list:
        data = data_path / fname
        f = group_to_list_generator(data, fname)
        tasks.add(asyncio.create_task(load_data(func=f)))
    await asyncio.gather(*tasks)




async def main():
    
    import time

    t0= time.time()
    await parser(url=URL, stop_year=STOP_YEAR)
    print(f"parsing time: {time.time() - t0}")

    t1 = time.time()
    await load_data_to_database(data_path,filename_list)
    print(f"loading to db time: {time.time() - t1}")
 
    print(f"total time: {time.time() - t0}")



asyncio.run(main())


