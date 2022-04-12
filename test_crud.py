import pytest
from app import app

test_user = "user_1"

data = {
    "article": f"article-{test_user}",
    "name": f"name {test_user}",
    "image_item": f"image-{test_user}",
    "price": 99,
    "currency": 866,
}

item_id = 1
accessToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0OTc2OTIyMCwianRpIjoiZGNlM2NmYmUtMmI1Yy00YTM0LWJkZGEtNzk4YTM5N2UxZGU0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjQ5NzY5MjIwLCJleHAiOjE2NTIzNjEyMjB9.cCu0OGg9JX_MhzUgYAfNJdEcE04zRWMwTxQPvCt_FAM"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {accessToken}",
}


@pytest.fixture
def client():
    app.config.update({"TESTING": True})

    with app.test_client() as client:
        yield client


def login_user(client):
    print(f"user: {test_user}")
    global headers

    resp = client.post(
        "/api/auth/signin", json={"username": "test1", "password": "test1"}
    )
    accessToken = resp.json["accessToken"]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {accessToken}",
    }
    # return headers


def create_item(client=None):
    # global item_id
    resp = client.post("/api/items", json=data, headers=headers)
    assert 200 == resp.status_code
    assert "ok" == resp.json["status"]
    assert "lastrowid" in resp.json
    assert 1 == resp.json["id"]
    # item_id = resp.json.get("lastrowid", 0)


def update_item(client=None):

    resp = client.put(f"/api/items/{item_id}", json=data, headers=headers)
    assert 200 == resp.status_code
    assert "ok" == resp.json["status"]
    assert 1 == resp.json["data"]


def delete_item(client=None):

    resp = client.delete(f"/api/items/{item_id}", headers=headers)
    assert 200 == resp.status_code
    assert "ok" == resp.json["status"]
    # assert "lastrowid" in resp.json
    assert 1 == resp.json["data"]


def show_item(client=None):

    resp = client.get(f"/api/items/{item_id}", headers=headers)
    assert 200 == resp.status_code
    assert "ok" == resp.json["status"]
    assert "data" in resp.json


def list_items(client=None, article=None, name=None):
    if article is not None:
        data = {"article": article}
    elif name is not None:
        data = {"q": name}
    resp = client.get("/api/items", query_string=data, headers=headers)
    assert 200 == resp.status_code
    assert "ok" == resp.json["status"]
    assert "data" in resp.json


# def test_login(client):
#     login_user(client)


def test_create_item(client):
    create_item(client)


def test_edit_item(client):
    data["id"] = item_id
    print(f"new item id: {item_id}")
    update_item(client=client)


def test_show_item(client):
    show_item(client=client)


def test_list_item(client):
    list_items(client=client, article=f"article-{test_user}")


def test_list_item2(client):
    list_items(client=client, name=f"name {test_user}")


def test_delete_item(client):
    delete_item(client=client)
