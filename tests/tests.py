from fastapi.testclient import TestClient
import pytest
from main import app


client = TestClient(app)


def test_del_authentication():
    response = client.delete('/delete_text/1')
    assert response.status_code == 401


def test_login():
    response = client.get('login')
    assert response.status_code == 200


def test_post_authentication():
    client.post('/put_text', json={'id': 1, 'text': 'przykladowy text'})
    response = client.get('/get_text/1')
    assert response.status_code == 200
    assert response.json() == {'id': 1,
                               'visit_counter': 1,
                               'text': 'przykladowy text'}