from fastapi.testclient import TestClient
import pytest
from main import app, get_only_letters
import datetime

client = TestClient(app)


def test_zad_1():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}


def test_zad_2():
    response = client.get("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "GET"}

    response = client.post("/method")
    assert response.status_code == 201
    assert response.json() == {"method": "POST"}

    response = client.delete("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "DELETE"}

    response = client.put("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "PUT"}

    response = client.options("/method")
    assert response.status_code == 200
    assert response.json() == {"method": "OPTIONS"}


@pytest.mark.parametrize("password, password_hash, status_code", [
    ('noga', '6f01b45d01cf324976ea079d86a8fdfc8d3b05d23e0ddecafaca3262c2ea2d76ba7267d436acb7ee114bceadcb7334b8349f434fe10923e1412b1a584cfc6632', 204),
    ('glowa', '1cd3b5b4f696c9f8b9ea6ab9f171945c3e10fdf7c85a90e718c137d72727ebe9f9ab7f51f4a3d79917a948e31f5c435dc2932fe772b70f5b387df9d844f0353c', 204),
    ('1234abcd', '249d582a7d42908f370f4c2fcb7060778b5e4aa0f05fd9d123995cdfb45ada5493b63ee1bde4d47ad0c5bf09a07a4714455d17bea38fc3c58afd89e4a5735a08', 204),
    ('żołądź', '9bb9c50519a6f74653dcaef519f4c86a9b7d85bb2dc928923e7df254990d1820c9dd9eb710c433cc7068e0b0807c32952bfc290817d04dff6cf7330e66d1022e', 204),
    (' jest ', 'c33d7c91055353fbf0ded85bf5938f7df085fc01dae1e35c7ce9b4c8b08b9ad3d676b92105787394f65cb8beb36309e1f8b89c1a196b72da08853cf7b605745c', 204),
    ('haslo', 'zly_hash', 401),
    ('', '', 401),
])
def test_zad_3(password, password_hash, status_code):
    print(password)
    print(password_hash)
    response = client.get(f'/auth?password={password}&password_hash={password_hash}')
    assert response.status_code == status_code


def test_zad_4():
    patient = {
        "name": "Patryk",
        "surname": "Jakubczak"
    }
    response = client.post(f"/register", json=patient)
    assert response.status_code == 201
    register_date = datetime.date.today()
    name_and_surname_sum = len(get_only_letters(patient["name"])) + len(get_only_letters(patient["surname"]))
    vaccination_date = register_date + datetime.timedelta(days=name_and_surname_sum)
    assert response.json() == {
        "id": 1,
        "name": "Patryk",
        "surname": "Jakubczak",
        "register_date": str(register_date),
        "vaccination_date": str(vaccination_date)
    }


@pytest.mark.parametrize("id, status_code",
                         [('1', 200), ('-1', 400), ('921834981274', 404)])
def test_get_patient_by_id(id, status_code):
    response = client.get(f"/patient/{id}")
    assert response.status_code == status_code
