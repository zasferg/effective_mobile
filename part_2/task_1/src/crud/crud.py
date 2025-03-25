from src.crud.base import Repository
from typing import TypeVar
from uuid import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from  src.models.models import *


Model = TypeVar("Model", bound=declarative_base())

    
class SqlalchemyRepository(Repository):
    
    def __init__(self, session: Session, model: Model):
        self.session = session
        self.model = model

    def get(self) -> list:
        try:
            with self.session as s:
                result = s.execute(select(self.model))
                return result.scalars().all()
        except Exception as e:
            raise e
    
    def get_by_id(self, record_id: UUID):
        try:
            with self.session as s:
                result = s.execute(select(self.model).where(self.model.id==record_id))
                return result.scalar_one_or_none()
        except Exception as e:
            raise e
    
    def update(self, record_id: UUID, **kwargs):
        try:
            with self.session as s:
                result = s.execute(update(self.model).where(self.model.id == record_id).values(**kwargs))
                s.commit()
                return result.scalar_one() 
        except Exception as e:
            raise e   

    def add(self, **kwargs):
        try:
            with self.session as s:
                entity = self.model(**kwargs)
                s.add(entity)
                s.commit()
                s.refresh(entity)
                return entity.__dict__
        except Exception as e:
            raise e
    
    def delete(self, record_id: UUID):
        try:    
            with self.session as s:
                s.execute(delete(self.model).where(self.model.id == record_id))
                s.commit()
        except Exception as e:
            raise e
        

class BooksCrud(SqlalchemyRepository):

    def get(self):
        try:
            with self.session as s:
                result = select(Book).join(Book.author).join(Book.genre)
                return s.scalars(result).all()
        except Exception as e:
            raise e
        