import pytest
from unittest.mock import patch, MagicMock
from services.memory import Memory

@patch('services.memory.chromadb.Client')
def test_ingest_happy_path(mock_client):
    # Arrange
    mock_collection = MagicMock()
    mock_client.return_value.create_collection.return_value = mock_collection
    memory = Memory()
    # Act
    result = memory.ingest([0.1, 0.2, 0.3], {'id': 1})
    # Assert
    assert result is True

@patch('services.memory.chromadb.Client')
def test_query_failure(mock_client):
    # Arrange
    mock_collection = MagicMock()
    mock_collection.query.side_effect = Exception('DB error')
    mock_client.return_value.create_collection.return_value = mock_collection
    memory = Memory()
    # Act
    result = memory.query([0.1, 0.2, 0.3])
    # Assert
    assert result is None 