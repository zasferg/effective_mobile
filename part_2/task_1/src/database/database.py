from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.models import Base
from src.settings import database_uri


engine = create_engine(database_uri)
Session = sessionmaker(bind=engine)

session = Session()

Base.metadata.create_all(engine)

