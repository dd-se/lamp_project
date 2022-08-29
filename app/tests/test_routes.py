from typing import List

from fastapi import FastAPI
from fastapi.testclient import TestClient

from database import User


def test_get_users(app: FastAPI, client: TestClient, test_users: List[User]):
    response = client.get(app.url_path_for("get_all_users"))
    data = response.text
    assert response.status_code == 200
    assert test_users[0].firstname in data
    assert test_users[1].firstname in data


def test_status(app: FastAPI, client: TestClient):
    response = client.get(app.url_path_for("status"))
    assert response.status_code == 200
