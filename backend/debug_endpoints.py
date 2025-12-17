import requests

try:
    # Test GET Key
    print("Testing GET /api/notifications/vapid-public-key...")
    r = requests.get("http://localhost:8000/api/notifications/vapid-public-key")
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text}")

    # Test POST Subscribe (con email invalido para que falle validacion o 404)
    print("\nTesting POST /api/notifications/subscribe...")
    r = requests.post("http://localhost:8000/api/notifications/subscribe?x_user_email=test", json={})
    print(f"Status: {r.status_code}") 
    # Esperamos 422 (validation error de body) o 404 (user not found) NO 404 (path not found)
except Exception as e:
    print(e)
