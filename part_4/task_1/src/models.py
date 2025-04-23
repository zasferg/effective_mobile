from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, Text, String, DateTime, func
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncAttrs

class Base(AsyncAttrs, DeclarativeBase):
    pass


class SpimexTradingResulsts(Base):

    __tablename__ = "spimex_trading_results"

    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    exchange_product_id: Mapped[str] = mapped_column(String(30),nullable=False)
    exchange_product_name: Mapped[str] = mapped_column(Text,nullable=False)
    oil_id: Mapped[str] = mapped_column(String(30),nullable=False)
    delivery_basis_name: Mapped[str] = mapped_column(Text,nullable=False)
    delivery_basis_id: Mapped[str] = mapped_column(String(30),nullable=True)
    delivery_type_id: Mapped[str] = mapped_column(String(30),nullable=True)
    volume: Mapped[int] = mapped_column(Integer, nullable=True)
    total: Mapped[int] = mapped_column(Integer, nullable=True)
    count: Mapped[int] = mapped_column(Integer, nullable=True)
    date: Mapped[datetime] = mapped_column(String(30))
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    updated_on: Mapped[datetime] = mapped_column(DateTime(),server_default=func.now(), onupdate=func.now())