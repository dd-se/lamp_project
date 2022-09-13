from typing import List, Union

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship, sessionmaker
from pydantic import BaseModel, Field

from settings import secrets

engine = create_engine(secrets.DATABASE_URL)
sync_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Movie(Base):
    __tablename__ = "movies"

    id: int = Column(Integer, primary_key=True, index=True)
    owner_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    title: str = Column(String(200), nullable=False)
    genre: str = Column(String(200), nullable=False)
    trailer: str = Column(String(200), unique=True)
    year: int = Column(Integer)


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String(20), nullable=False, unique=True)
    firstname: str = Column(String(20), nullable=False)
    lastname: str = Column(String(20), nullable=False)
    password: str = Column(String(120))

    movies: List[Movie] = relationship("Movie", order_by="desc(Movie.genre)")


def get_db() -> Session:
    with sync_session() as session:
        yield session


# schema validator
class MovieIn(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    genre: str = Field(min_length=3, max_length=200)
    trailer: Union[str, None]
    year: Union[int, None] = None

    class Config:
        orm_mode = True
        anystr_strip_whitespace = True
