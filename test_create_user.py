import os
import tempfile

import pytest

from app import app

test_user = f"user_2"

item_id = 1
accessToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0OTY4NDIwNiwianRpIjoiNzY0NmQxYTMtM2NlOC00MGJiLTlmMDItOTJhZjkzZjIyMWZlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjQ5Njg0MjA2LCJleHAiOjE2NTIyNzYyMDZ9.rq1Wz9yHa8CefIPbVh_oUI4hegNFXGla_0qXvJZELm8"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {accessToken}",
}


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


def edit_user(client, test_user):

    resp = client.put(
        "/api/auth/edit",
        json={"username": "new_" + test_user, "avatar": "avatar_" + test_user},
        headers=headers,
    )
    assert 200 == resp.status_code
    assert f"User {'new_' + test_user} edited OK" == resp.json["message"]
    assert "ok" == resp.json["status"]


def test_create_user(client):

    create_user(client, test_user)


def test_login_user(client):

    login_user(client, test_user)


def test_edit_user(client):

    edit_user(client, test_user)
