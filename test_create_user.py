import os
import tempfile

import pytest

from app import app

test_user = f"user_2"


@pytest.fixture
def client():
    app.config.update({"TESTING": True})

    with app.test_client() as client:
        yield client


def test_helloworld_page(client):

    resp = client.get("/")
    assert b"Hello world" in resp.data


def create_user(client, test_user):

    resp = client.post(
        "/api/auth/signup", json={"username": test_user, "password": test_user}
    )
    assert 200 == resp.status_code
    assert f"create user {test_user} Ok" == resp.json["message"]
    assert "ok" == resp.json["status"]
    assert "accessToken" in resp.json
    assert test_user == resp.json["username"]
    return resp.json.get("accessToken", "")


def login_user(client, test_user):

    resp = client.post(
        "/api/auth/signin", json={"username": test_user, "password": test_user}
    )
    assert 200 == resp.status_code
    assert f"Login user {test_user} Ok" == resp.json["message"]
    assert "ok" == resp.json["status"]
    assert "accessToken" in resp.json
    assert test_user == resp.json["username"]
    return resp.json.get("accessToken", "")


def test_create_user(client):

    create_user(client, test_user)


def test_login_user(client):

    login_user(client, test_user)
