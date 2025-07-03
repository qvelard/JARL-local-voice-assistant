import pytest
from unittest.mock import patch, mock_open
from core.utils import load_config, load_json_schema

@patch('builtins.open', new_callable=mock_open, read_data='foo: bar')
@patch('services.utils.yaml.safe_load', return_value={'foo': 'bar'})
def test_load_config_happy_path(mock_yaml, mock_file):
    config = load_config()
    assert config == {'foo': 'bar'}

@patch('builtins.open', side_effect=Exception('File error'))
def test_load_config_failure(mock_file):
    config = load_config()
    assert config == {}

@patch('builtins.open', new_callable=mock_open, read_data='{"type": "object"}')
def test_load_json_schema_happy_path(mock_file):
    with patch('services.utils.json.load', return_value={'type': 'object'}):
        schema = load_json_schema('dummy.json')
        assert schema == {'type': 'object'}

@patch('builtins.open', side_effect=Exception('File error'))
def test_load_json_schema_failure(mock_file):
    schema = load_json_schema('dummy.json')
    assert schema == {} 