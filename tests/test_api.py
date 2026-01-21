from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from backend.api import app
from backend.llm_handler import get_llm_handler
from backend.vector_db import get_vector_db

client = TestClient(app)

# Mocks
mock_llm = MagicMock()
mock_llm.is_ready.return_value = True
mock_llm.generate_response.return_value = "Mocked response"

mock_vdb = MagicMock()
mock_vdb.is_connected = True
mock_vdb.get_context_for_query.return_value = "Mocked context"

# Dependency overrides
app.dependency_overrides[get_llm_handler] = lambda: mock_llm
app.dependency_overrides[get_vector_db] = lambda: mock_vdb

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_chat_endpoint():
    response = client.post("/chat", json={"message": "Hello"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["response"] == "Mocked response"
    assert data["context_used"] is True

def test_chat_empty_message():
    response = client.post("/chat", json={"message": ""})
    assert response.status_code == 400
