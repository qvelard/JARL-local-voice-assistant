import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from services.orchestrator import app, Orchestrator

@patch('services.orchestrator.requests.post')
def test_plan_endpoint_happy_path(mock_post):
    # Arrange
    mock_post.return_value = MagicMock(status_code=200, json=lambda: {'step': 'do something'})
    client = TestClient(app)
    # Act
    response = client.post('/plan', json={'user_input': 'turn on the light'})
    # Assert
    assert response.status_code == 200
    assert 'plan' in response.json()

@patch('services.orchestrator.requests.post')
def test_plan_endpoint_llm_failure(mock_post):
    # Arrange
    mock_post.side_effect = Exception('LLM down')
    client = TestClient(app)
    # Act
    response = client.post('/plan', json={'user_input': 'turn on the light'})
    # Assert
    assert response.status_code == 500 