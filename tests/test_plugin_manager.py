import pytest
from unittest.mock import patch, MagicMock
from services.plugin_manager import PluginManager

@patch('services.plugin_manager.os.listdir')
def test_discover_skills_happy_path(mock_listdir):
    # Arrange
    mock_listdir.return_value = ['foo.py', 'bar.py', '__init__.py']
    manager = PluginManager()
    # Act
    skills = manager.discover_skills()
    # Assert
    assert set(skills) == {'foo', 'bar'}

@patch('services.plugin_manager.os.listdir')
def test_discover_skills_failure(mock_listdir):
    # Arrange
    mock_listdir.side_effect = Exception('IO error')
    manager = PluginManager()
    # Act
    skills = manager.discover_skills()
    # Assert
    assert skills == [] 