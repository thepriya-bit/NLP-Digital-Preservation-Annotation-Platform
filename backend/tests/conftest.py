from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def app():
    from app.main import app
    return app


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def auth_headers(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "testadmin",
            "email": "admin@test.com",
            "password": "testpass123",
            "role": "admin",
        },
    )
    if response.status_code == 201:
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/auth/login",
        json={"username": "testadmin", "password": "testpass123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def annotator_headers(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "testannotator",
            "email": "annotator@test.com",
            "password": "testpass123",
            "role": "annotator",
        },
    )
    if response.status_code == 201:
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/auth/login",
        json={"username": "testannotator", "password": "testpass123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def verifier_headers(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "testverifier",
            "email": "verifier@test.com",
            "password": "testpass123",
            "role": "verifier",
        },
    )
    if response.status_code == 201:
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/auth/login",
        json={"username": "testverifier", "password": "testpass123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
