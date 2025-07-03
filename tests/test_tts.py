import pytest
from unittest.mock import patch, MagicMock
from services.tts import TextToSpeech

@pytest.mark.asyncio
@patch('services.tts.CoquiTTS')
async def test_speak_happy_path(mock_coqui):
    # Arrange
    mock_tts = MagicMock()
    mock_tts.tts.return_value = b'audio'
    mock_tts.play.return_value = None
    mock_coqui.return_value = mock_tts
    tts = TextToSpeech()
    # Act
    result = await tts.speak('hello')
    # Assert
    assert result == b'audio'

@pytest.mark.asyncio
@patch('services.tts.CoquiTTS')
async def test_speak_failure(mock_coqui):
    # Arrange
    mock_tts = MagicMock()
    mock_tts.tts.side_effect = Exception('TTS error')
    mock_coqui.return_value = mock_tts
    tts = TextToSpeech()
    # Act
    result = await tts.speak('hello')
    # Assert
    assert result is None 