import os
import sys
from typing import Any, Generator, List

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import Base, User, get_db
from api import router

_app = FastAPI()
_app.include_router(router)
engine = create_engine(url="sqlite://", connect_args={"check_same_thread": False})
sync_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def app() -> Generator[FastAPI, Any, None]:
    Base.metadata.create_all(engine)
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def db_session(app: FastAPI) -> Generator[Session, Any, None]:
    with engine.connect() as connection:
        transaction = connection.begin()
        with sync_session(bind=connection) as session:
            yield session
        transaction.rollback()


@pytest.fixture(scope="module")
def client(app: FastAPI, db_session: Session) -> Generator[TestClient, Any, None]:
    def get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = get_test_db

    with TestClient(app=app) as client:
        yield client


@pytest.fixture(scope="module")
def test_users(app: FastAPI, db_session: Session) -> Generator[List[User], Any, None]:
    first_user = User(
        username="firstuser",
        firstname="firstname",
        lastname="lastname",
        password="pass",
    )
    second_user = User(
        username="seconduser",
        firstname="secondfirstname",
        lastname="secondlastname",
        password="pass",
    )
    db_session.add_all([first_user, second_user])
    db_session.commit()
    yield first_user, second_user
