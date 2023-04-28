import pytest
from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime, timedelta
import random

client = TestClient(app)

# Mock data for datetime
dt = datetime.now() - timedelta(days=random.randint(1, 7))
dt = dt.replace(hour=3, minute=30)


def test_get_food():
    response = client.get(f"/get_food?meal_time={dt.isoformat()}")
    assert response.status_code == 200
    assert isinstance(response.json(), list) or response.json() == "Nothing open!"
