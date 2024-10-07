from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={
        "nombre": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123456789",
        "balance": 500000
    })
    assert response.status_code == 200
    assert response.json()["success"] == True
