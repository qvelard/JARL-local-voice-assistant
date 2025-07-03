import pytest
from unittest.mock import patch, MagicMock
from services.action_dispatcher import ActionDispatcher

@patch('services.action_dispatcher.subprocess.run')
def test_dispatch_happy_path(mock_run):
    # Arrange
    mock_run.return_value = MagicMock(returncode=0, stdout='ok', stderr='')
    dispatcher = ActionDispatcher()
    step = {'command': 'echo ok'}
    # Act
    result = dispatcher.dispatch(step)
    # Assert
    assert result == 0

@patch('services.action_dispatcher.subprocess.run')
def test_dispatch_missing_command(mock_run):
    dispatcher = ActionDispatcher()
    step = {}
    result = dispatcher.dispatch(step)
    assert result is None 