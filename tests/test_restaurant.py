from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_restaurants():
    # Send a GET request to the /restaurants/ endpoint
    response = client.get("/restaurants/")

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Optionally, you can check the response content or perform more specific assertions
    # For example, you can assert that the response contains a list of restaurants
    assert isinstance(response.json(), list)
