import pytest
from unittest.mock import patch, MagicMock
import numpy as np
from services.stt import SpeechToText

@patch('services.stt.whisper')
def test_transcribe_happy_path(mock_whisper):
    # Arrange
    mock_model = MagicMock()
    mock_model.transcribe.return_value = {'text': 'hello world'}
    mock_whisper.load_model.return_value = mock_model
    stt = SpeechToText()
    audio = np.zeros(16000, dtype='float32')
    # Act
    result = stt.transcribe(audio)
    # Assert
    assert result == 'hello world'

@patch('services.stt.whisper')
def test_transcribe_failure(mock_whisper):
    # Arrange
    mock_model = MagicMock()
    mock_model.transcribe.side_effect = Exception('STT error')
    mock_whisper.load_model.return_value = mock_model
    stt = SpeechToText()
    audio = np.zeros(16000, dtype='float32')
    # Act
    result = stt.transcribe(audio)
    # Assert
    assert result is None 