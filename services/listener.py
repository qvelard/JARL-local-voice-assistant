"""
Listener module for hotkey/wake-word detection and audio recording.
"""
from typing import Optional
import numpy as np
import sounddevice as sd
from services.utils import logger, load_config

class Listener:
    """
    Handles hotkey or wake-word detection and records audio chunks.
    """
    def __init__(self) -> None:
        self.config = load_config()
        self.samplerate: int = self.config.get('listener', {}).get('samplerate', 16000)
        self.channels: int = self.config.get('listener', {}).get('channels', 1)
        self.duration: float = self.config.get('listener', {}).get('duration', 3.0)  # seconds

    def record_audio(self) -> Optional[np.ndarray]:
        """
        Records an audio chunk from the default microphone.

        Returns:
            np.ndarray: The recorded audio waveform, or None if recording fails.
        """
        try:
            logger.info(f"Recording audio: {self.duration}s @ {self.samplerate}Hz, {self.channels} channel(s)")
            audio = sd.rec(int(self.duration * self.samplerate), samplerate=self.samplerate, channels=self.channels, dtype='float32')
            sd.wait()
            return audio.flatten()
        except Exception as e:
            logger.error(f"Audio recording failed: {e}")
            return None 