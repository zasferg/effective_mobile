from src.schemas.trade import SpimexTradeResultGet
from src.models.models import SpimexTradingResulsts
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime


class TradeCrud:

    base_model = SpimexTradingResulsts
    get_schema = SpimexTradeResultGet

    @classmethod
    async def get_all(cls, session: AsyncSession):
        res = await session.execute(select(cls.base_model).limit(10))

        objects = res.scalars().all()

        return  [cls.get_schema.model_validate(obj) for obj in objects]
    

    @classmethod
    async def get_last_trading_dates(cls, session: AsyncSession, start_date: datetime):

        res = await session.execute(
            select(cls.base_model.date)
            .where(func.to_date(cls.base_model.date, 'DD.MM.YYYY') >= start_date).order_by(cls.base_model.date)
        )

        objects = res.scalars().all()
        return objects
    
    @classmethod
    async def get_dynamics(cls, session: AsyncSession, start_date: datetime, end_date: datetime, **kwargs):

        clean_kwargs = {key: value for key, value in kwargs.items() if value is not None}
        
        # res = await session.execute(select(cls.base_model)
        #                             .where(func.to_date(cls.base_model.date, 'DD.MM.YYYY') >= start_date)
        #                             .where(func.to_date(cls.base_model.date, 'DD.MM.YYYY') <= end_date)
        #                             .filter_by(**clean_kwargs)
        #                             .order_by(cls.base_model.date))

        query = (
                select(cls.base_model)
                .filter(
                    func.to_date(cls.base_model.date, 'DD.MM.YYYY').between(start_date, end_date),
                    *[getattr(cls.base_model, key) == value for key, value in clean_kwargs.items()]
                )
                .order_by(cls.base_model.date)
            )
        res = await session.execute(query)
        objects = res.scalars().all()
        return [cls.get_schema.model_validate(obj) for obj in objects]
    
    @classmethod
    async def get_trading_results(cls, session: AsyncSession, start_date: datetime, **kwargs):
        clean_kwargs = {key: value for key, value in kwargs.items() if value is not None}
        res = await session.execute(select(cls.base_model)
                                 .where(func.to_date(cls.base_model.date, 'DD.MM.YYYY') >= start_date)
                                 .filter_by(**clean_kwargs).order_by(cls.base_model.date))
        
        objects = res.scalars().all()
        return [cls.get_schema.model_validate(obj) for obj in objects]