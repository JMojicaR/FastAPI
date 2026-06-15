from fastapi.testclient import TestClient
from intermedio import app

client = TestClient(app)

def test_get_user_success():
    response = client.get("/users/user1", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {"id": "user1", "username": "user1", "email": "email1"}

def test_get_user_unauthorized():
    response = client.get("/users/user1", headers={"X-Token": "wrongtoken"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid X-Token header"}

def test_get_user_not_found():
    response = client.get("/users/nonexistent", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_success():
    new_user = {"id": "user3", "username": "user3", "email": "email3"}
    response = client.post("/users/", json=new_user, headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == new_user

def test_create_user_unauthorized():
    new_user = {"id": "user4", "username": "user4", "email": "email4"}
    response = client.post("/users/", json=new_user, headers={"X-Token": "wrongtoken"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid X-Token header"}

def test_create_user_already_exists():
    existing_user = {"id": "user1", "username": "user1", "email": "email1"}
    response = client.post("/users/", json=existing_user, headers={"X-Token": "coneofsilence"})
    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}