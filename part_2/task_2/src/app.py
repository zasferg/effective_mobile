from src.utils.xml import group_to_list_generator
import os
from pathlib import Path
from src.utils.loader import SqlAlchemySpimexTradingResulstsRepository
from src.models import SpimexTradingResulsts
from src.database import session
import pandas as pd
from src.settings import URL, STOP_YEAR
from src.parser.parser import parser
from src.settings import data_path

filename_list = os.listdir(data_path)


def load_data_to_database(data_path: str,fname_list: list ):
    data_loader = SqlAlchemySpimexTradingResulstsRepository(session=session,model=SpimexTradingResulsts)
    for fname in fname_list:
        data = data_path / fname
        f = group_to_list_generator(data, fname)
        while True:
            try:
                data_row = next(f)
                print(data_row)
                if  not any(pd.isna(item) for item in data_row):
                    data_loader.load(data=data_row)
                
            except StopIteration:
                break



parser(url=URL, stop_year=STOP_YEAR)
load_data_to_database(data_path,filename_list)
