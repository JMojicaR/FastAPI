from fastapi.testclient import TestClient
import pytest
from avanzado import MockDatabase, app, get_db

client = TestClient(app)

# Fixtures

@pytest.fixture()
def testdb():
    return MockDatabase()

@pytest.fixture()
def client_with_db(testdb):
    async def override_get_db():
        yield testdb
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture
def sample_data():
    return {"key": "item3", "value": {"name": "Item 3", "price": 30.0}}


# Tests

def test_create_item_success(client_with_db, sample_data):
    response = client_with_db.post("/data/", json=sample_data)
    assert response.status_code == 200
    assert response.json() == {"name": "Item 3", "price": 30.0}

def test_create_item_missing_fields(client_with_db):
    response = client_with_db.post("/data/", json={"key": "item4"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Key and value are required"}

def test_create_item_already_exists(client_with_db):
    existing_data = {"key": "item1", "value": {"name": "Item 1", "price": 10.0}}
    response = client_with_db.post("/data/", json=existing_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Key already exists"}

def test_read_data(client_with_db):
    response = client_with_db.get("/data/item1")
    assert response.status_code == 200
    assert response.json() == {"name": "Item 1", "price": 10.0}

def test_read_data_not_found(client_with_db):
    response = client_with_db.get("/data/nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Key not found"}

def test_update_data(client_with_db, sample_data):
    response = client_with_db.post("/data/", json=sample_data)
    assert response.status_code == 200
    assert response.json() == {"name": "Item 3", "price": 30.0}

def test_update_data_missing_fields(client_with_db):
    response = client_with_db.post("/data/", json={"key": "item4"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Key and value are required"}

def test_update_data_already_exists(client_with_db):
    existing_data = {"key": "item1", "value": {"name": "Item 1", "price": 10.0}}
    response = client_with_db.post("/data/", json=existing_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Key already exists"}

