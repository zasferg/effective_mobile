from src.models import SpimexTradingResulsts
from sqlalchemy.orm import Session
from sqlalchemy import select

class SqlAlchemySpimexTradingResulstsRepository:

   
    def __init__(self, session: Session, model: SpimexTradingResulsts):
        self.model = model
        self.session = session

    def load(self ,data: list):
        try:
            with self.session as s:
                entity = SpimexTradingResulsts(
                    exchange_product_id=data[0],
                    exchange_product_name=data[1],
                    oil_id = data[0][:4],
                    delivery_basis_id=data[0][4:7],
                    delivery_basis_name=data[2],
                    delivery_type_id=data[0][-1],
                    volume=data[3],
                    total=data[4],
                    date=data[14],
                    count=data[13]

                )
                s.add(entity)
                s.commit()
                s.refresh(entity)
        except Exception as e:
            raise e
    
    def get(self,):
        with self.session as s:
            result = s.execute(select(self.model))
            return result.scalars().all()

    