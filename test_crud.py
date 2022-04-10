import os
import tempfile

import pytest

from app import app


@pytest.fixture
def client():
    app.config.update({'TESTING': True})

    with app.test_client() as client:
        yield client

def create_item(client=None,data=None,headers=None):

    resp = client.post('/api/items',json=data,headers=headers)
    assert 200 == resp.status_code
    assert 'ok' == resp.json["status"]       
    assert "lastrowid" in resp.json  
    assert 1 == resp.json["id"]  
    return resp.json.get("lastrowid",0)  


def update_item(client=None,item_id=None,data=None,headers=None):

    resp = client.put(f'/api/items/{item_id}',json=data,headers=headers)
    assert 200 == resp.status_code
    assert 'ok' == resp.json["status"]       
    assert 1 == resp.json["data"]  
  

def delete_item(client=None,item_id=None,headers=None):

    resp = client.delete(f'/api/items/{item_id}',headers=headers)
    assert 200 == resp.status_code
    assert 'ok' == resp.json["status"]       
    # assert "lastrowid" in resp.json  
    assert 1 == resp.json["data"]  


def show_item(client=None,item_id=None,headers=None):

    resp = client.get(f'/api/items/{item_id}',headers=headers)
    assert 200 == resp.status_code
    assert 'ok' == resp.json["status"]       
    assert 'data' in resp.json

def list_items(client=None,article=None,name=None,headers=None):
    if article is not None:
        data={"article":article}
    elif name is not None:
        data = {"name":name}
    resp = client.get('/api/items',json=data,headers=headers)
    assert 200 == resp.status_code
    assert 'ok' == resp.json["status"]       
    assert 'data' in resp.json


def test_item(client):

    test_user='test4'
    print(f"user: {test_user}")

    resp=client.post('/api/auth/signin',json={"username":"test1","password":"test1"})
    accessToken = resp.json["accessToken"]
    headers={"Content-Type": "application/json", "Authorization": f"Bearer {accessToken}"}    


    data={"article":f"article-{test_user}","name":f"name {test_user}","image_item":f"image-{test_user}","price":99,"currency":866}
    item_id = create_item(client=client,data=data,headers=headers)
    data["id"]=item_id
    print(f"new item id: {item_id}")
    update_item(client=client,item_id=item_id,data=data,headers=headers)  
    show_item(client=client,item_id=item_id,headers=headers)  
    list_items(client=client,article=f"article-{test_user}",headers=headers)
    list_items(client=client,name=f"name {test_user}",headers=headers)
    delete_item(client=client,item_id=item_id)  

      


