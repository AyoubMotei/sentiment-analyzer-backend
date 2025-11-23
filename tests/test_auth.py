from fastapi.testclient import TestClient
import os
import jwt as pyjwt

# importer l'app et les fonctions
from app.main import app

client = TestClient(app)

def setup_module():
    # config minimal pour les tests
    os.environ["JWT_SECRET"] = "testsecret"
    os.environ["ALGORITHM"] = "HS256"
    os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "60"

def test_login_success():
    resp = client.post("/login", json={"username": "admin", "password": "admin123"})
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["username"] == "admin"

def test_login_failure():
    resp = client.post("/login", json={"username": "admin", "password": "wrong"})
    assert resp.status_code == 401
