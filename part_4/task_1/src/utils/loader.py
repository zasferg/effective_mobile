from src.models import SpimexTradingResulsts
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class SqlAlchemySpimexTradingResulstsRepository:

   
    def __init__(self, session: AsyncSession, model: SpimexTradingResulsts):
        self.model = model
        self.session = session

    async def load(self ,data: list):
        try:
            async with self.session() as s:
                entity = SpimexTradingResulsts(
                    exchange_product_id=data[0],
                    exchange_product_name=data[1],
                    oil_id = data[0][:4],
                    delivery_basis_id=data[0][4:7],
                    delivery_basis_name=data[2],
                    delivery_type_id=data[0][-1],
                    volume=int(data[3]),
                    total=int(data[4]),
                    date=data[14],
                    count=int(data[13])

                )
                s.add(entity)
                await s.commit()
                await s.refresh(entity)
        except Exception as e:
            raise e
    
    async def get(self,):
        async with self.session() as s:
            result = await s.execute(select(self.model))
            return result.scalars().all()

    