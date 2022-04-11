import os
import tempfile

import pytest

from app import app


@pytest.fixture
def client():
    app.config.update({'TESTING': True})

    with app.test_client() as client:
        yield client


def test_helloworld_page(client):

    resp = client.get('/')
    assert b'Hello world' in resp.data        


def create_user(client,test_user):

    # test_user='test5'

    resp = client.post('/api/auth/signup',json={"username":test_user,"password":test_user})
    assert 200 == resp.status_code
    assert f'create user {test_user} Ok' == resp.json["message"]
    assert 'ok' == resp.json["status"]       
    assert "accessToken" in resp.json  
    assert test_user == resp.json["username"]  
    return resp.json.get("accessToken","")  


def login_user(client,test_user):

    resp = client.post('/api/auth/signin',json={"username":test_user,"password":test_user})
    assert 200 == resp.status_code
    assert f"Login user {test_user} Ok" == resp.json["message"]
    assert 'ok' == resp.json["status"]       
    assert "accessToken" in resp.json  
    assert test_user == resp.json["username"] 
    return resp.json.get("accessToken","")  

def test_login_user(client):
    users=[]
    for u in range(1,5):
        test_user=f"test{u}"
        accessToken = create_user(client,test_user)
        accessToken = login_user(client,test_user)  
        users.append([test_user,accessToken])
    
    with open('users.txt','a',encoding="utf8") as f:
        for u in users:
            f.write(f"{u[0]},{u[1]},\n")  
       


