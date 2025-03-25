from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, func, DECIMAL, UUID
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Author(Base):
    __tablename__ = "author"
 
    id = Column(UUID, primary_key=True, nullable=False)
    name_author = Column(String(100), nullable=False)

    books = relationship("Book", back_populates="author",lazy='selectin')


class Genre(Base):
    __tablename__= "genre"

    id = Column(UUID, primary_key=True, nullable=False)
    name_genre = Column(String(30), nullable=False)

    books = relationship("Book", back_populates="genre", lazy='selectin')


class Book(Base):
    __tablename__ = "book"

    id = Column(UUID, primary_key=True, nullable=False)
    title = Column(String(255), nullable=False)
    author_id = Column(UUID, ForeignKey("author.id"), nullable=True)
    genre_id = Column(UUID, ForeignKey("genre.id"), nullable=True)

    author = relationship("Author", back_populates="books", lazy='selectin')
    genre = relationship("Genre", back_populates="books", lazy='selectin')
    buy_books = relationship("BuyBook", back_populates="book",lazy='selectin')


class City(Base):
    __tablename__ = "city"

    id = Column(UUID, primary_key=True, nullable=False)
    name_city = Column(String(30), nullable=False)
    days_delivery = Column(DECIMAL, nullable=False)

    clients = relationship("Client", back_populates="city")


class Client(Base):
    __tablename__ = "client"

    id = Column(UUID, primary_key=True, nullable=False)
    name_client = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    city_id = Column(UUID, ForeignKey("city.id"), nullable=False)

    city = relationship("City", back_populates="clients")
    buys = relationship("Buy", back_populates="client")


class Buy(Base):
    __tablename__ = "buy"

    id = Column(UUID, primary_key=True, nullable=False)
    buy_descr = Column(String(255), nullable=True)
    client_id = Column(UUID, ForeignKey("client.id"), nullable=False)

    client = relationship("Client", back_populates="buys")
    buy_books = relationship("BuyBook", back_populates="buy")
    buy_steps = relationship("BuyStep", back_populates="buy")


class BuyBook(Base):
    __tablename__ = "buy_book"

    id = Column(UUID, primary_key=True, nullable=False)
    buy_id = Column(UUID, ForeignKey("buy.id"), nullable=False)
    book_id = Column(UUID, ForeignKey("book.id"), nullable=False)
    amount = Column(DECIMAL, nullable=False)

    buy = relationship("Buy", back_populates="buy_books")
    book = relationship("Book", back_populates="buy_books")


class Step(Base):
    __tablename__ = "step"

    id = Column(UUID, primary_key=True, nullable=False)
    name_step = Column(String(100), nullable=False)

    buy_steps = relationship("BuyStep", back_populates="step")


class BuyStep(Base):
    __tablename__ = "buy_step"

    id = Column(UUID, primary_key=True, nullable=False)
    buy_id = Column(UUID, ForeignKey("buy.id"), nullable=False)
    step_id = Column(UUID, ForeignKey("step.id"), nullable=False)
    date_step_beg = Column(TIMESTAMP, server_default=func.now())
    date_step_end = Column(TIMESTAMP, nullable=True)

    buy = relationship("Buy", back_populates="buy_steps")
    step = relationship("Step", back_populates="buy_steps")
