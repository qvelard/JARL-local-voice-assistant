"""
TTS module for text-to-speech synthesis.
"""
from typing import Optional
from TTS.api import TTS as CoquiTTS
from services.utils import logger, load_config
import asyncio

class TextToSpeech:
    """
    Wraps Coqui-TTS to synthesize and play audio from text.
    """
    def __init__(self) -> None:
        self.config = load_config()
        self.model_name: str = self.config.get('tts', {}).get('model', 'tts_models/en/ljspeech/tacotron2-DDC')
        try:
            self.tts = CoquiTTS(self.model_name)
        except Exception as e:
            logger.error(f"Failed to load TTS model: {e}")
            raise

    async def speak(self, text: str) -> Optional[bytes]:
        """
        Synthesizes speech from text and plays it.

        Args:
            text (str): Text to synthesize.

        Returns:
            Optional[bytes]: The raw audio data, or None if failed.
        """
        try:
            logger.info(f"Synthesizing speech for: {text}")
            audio = await asyncio.to_thread(self.tts.tts, text)
            await asyncio.to_thread(self.tts.play, audio)
            return audio
        except Exception as e:
            logger.error(f"TTS synthesis failed: {e}")
            return None 