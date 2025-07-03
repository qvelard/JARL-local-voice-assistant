"""
Tests for the Listener module.
Covers audio recording functionality, including normal and failure cases.
"""
import pytest
from unittest.mock import patch, MagicMock
import numpy as np
from core.listener import Listener

@patch('services.listener.sd')
def test_record_audio_happy_path(mock_sd):
    # Arrange
    mock_audio = np.ones((48000, 1), dtype='float32')
    mock_sd.rec.return_value = mock_audio
    mock_sd.wait.return_value = None
    listener = Listener()
    listener.duration = 3.0
    listener.samplerate = 16000
    listener.channels = 1
    # Act
    result = listener.record_audio()
    # Assert
    assert isinstance(result, np.ndarray)
    assert result.shape[0] == 48000

@patch('services.listener.sd')
def test_record_audio_failure(mock_sd):
    # Arrange
    mock_sd.rec.side_effect = Exception('Microphone error')
    listener = Listener()
    # Act
    result = listener.record_audio()
    # Assert
    assert result is None 