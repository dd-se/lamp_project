from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from settings import secrets

engine = create_engine(secrets.DATABASE_URL)
sync_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String(20), nullable=False, unique=True)
    firstname: str = Column(String(20), nullable=False)
    lastname: str = Column(String(20), nullable=False)
    password: str = Column(String(120))


def get_db() -> Session:
    with sync_session() as session:
        yield session
