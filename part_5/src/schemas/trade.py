from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True


class SpimexTradeResultCreate(BaseSchema):
    id: int
    exchange_product_id: str
    exchange_product_name: str
    oil_id: str
    delivery_basis_name: str
    delivery_basis_id: Optional[str] = None
    delivery_type_id: Optional[str] = None
    volume: Optional[int] = None
    total: Optional[int] = None
    count: Optional[int] = None
    date: str


class SpimexTradeResultUpdate(SpimexTradeResultCreate):
    pass


class SpimexTradeResultGet(SpimexTradeResultCreate):
    id: int
    created: datetime
    updated_on: datetime

