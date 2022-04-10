import os
import tempfile

import pytest

from app import app


@pytest.fixture
def client():
    app.config.update({'TESTING': True})

    with app.test_client() as client:
        yield client


def create_item(client,data):

    # test_user='test5'

    resp = client.post('/api/items',json=data)
    assert 200 == resp.status_code
    assert 'ok' == resp.json["status"]       
    assert "lastrowid" in resp.json  
    assert 1 == resp.json["rowcount"]  
    return resp.json.get("lastrowid",0)  


def update_item(client,data):

    # test_user='test5'

    resp = client.post('/api/items',json=data)
    assert 200 == resp.status_code
    assert 'ok' == resp.json["status"]       
    assert "lastrowid" in resp.json  
    assert 1 == resp.json["rowcount"]  
    return resp.json.get("lastrowid",0)   

def delete_item(client,data):

    # test_user='test5'

    resp = client.post('/api/items',json=data)
    assert 200 == resp.status_code
    assert 'ok' == resp.json["status"]       
    # assert "lastrowid" in resp.json  
    assert 1 == resp.json["rowcount"]  
    return resp.json.get("lastrowid",0)    


def show_item(client,data):

    # test_user='test5'

    resp = client.post('/api/items',json=data)
    assert 200 == resp.status_code
    assert 'ok' == resp.json["status"]       
    # assert "lastrowid" in resp.json  
    # assert 1 == resp.json["rowcount"]  
    # return resp.json.get("lastrowid",0)    

def list_items(client,data):

    # test_user='test5'

    resp = client.post('/api/items',json=data)
    assert 200 == resp.status_code
    assert 'ok' == resp.json["status"]       
    assert "lastrowid" in resp.json  
    assert 1 == resp.json["rowcount"]  
    return resp.json.get("lastrowid",0)       


def test_item(client):
    with open("users.txt") as f:
        users=f.readlines()
    for i,u in enumerate(users,1):
        test_user=','.split(u)[0]
        print(f"user: {test_user}")
        resp = client.post('/api/auth/signin',json={"username":test_user,"password":test_user})
 
        data={"article":f"article-{u}","name":f"name {u}","image_item":f"image-{u}","price":i,"currency":866}
        item_id = create_item(client,data)
        data["id"]=item_id
        print(f"new item id: {item_id}")
        # update_item(client,test_user,data)  
        # show_item(client,test_user,item_id)  
        # list_items(client,test_user,article=f"article-{u}")
        # list_items(client,test_user,name=f"name {u}"f"article-{u}")
        # delete_item(client,test_user,item_id)  

      


