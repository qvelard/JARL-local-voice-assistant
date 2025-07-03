"""
STT module for speech-to-text using Whisper.
"""
from typing import Optional
import numpy as np
import whisper
from services.utils import logger, load_config

class SpeechToText:
    """
    Wraps Whisper to transcribe audio numpy arrays to text.
    """
    def __init__(self) -> None:
        self.config = load_config()
        self.model_name: str = self.config.get('stt', {}).get('model', 'base')
        try:
            self.model = whisper.load_model(self.model_name)
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            raise

    def transcribe(self, audio: np.ndarray, samplerate: int = 16000) -> Optional[str]:
        """
        Transcribes the given audio numpy array to text.

        Args:
            audio (np.ndarray): Audio waveform.
            samplerate (int): Sample rate of the audio.

        Returns:
            Optional[str]: Transcribed text, or None if failed.
        """
        try:
            logger.info("Transcribing audio with Whisper...")
            result = self.model.transcribe(audio, fp16=False, language='en', task='transcribe', sampling_rate=samplerate)
            return result.get('text', '').strip()
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            return None 