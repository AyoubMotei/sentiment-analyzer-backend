import requests

BASE_URL = "http://127.0.0.1:8000"

#  Login
print("1. Test Login...")
response = requests.post(f"{BASE_URL}/login", json={
    "username": "admin",
    "password": "admin123"
})
print(f"Status: {response.status_code}")
data = response.json()
print(f"Response: {data}")

token = data["access_token"]
print(f"\nToken obtenu: {token[:50]}...\n")

#  Predict
print("2. Test Predict...")
response = requests.post(
    f"{BASE_URL}/predict",
    json={"text": "i love this product"},
    headers={"Authorization": f"Bearer {token}"}
)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")