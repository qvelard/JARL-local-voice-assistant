"""
Action dispatcher module for executing plan steps.
"""
from typing import Dict, Any, Optional
import subprocess
from services.utils import logger, load_config

class ActionDispatcher:
    """
    Maps plan steps to subprocess or OS calls.
    """
    def __init__(self) -> None:
        self.config = load_config()

    def dispatch(self, step: Dict[str, Any]) -> Optional[int]:
        """
        Executes a plan step as a subprocess command.

        Args:
            step (Dict[str, Any]): Plan step with 'command' key.

        Returns:
            Optional[int]: Return code of the subprocess, or None if failed.
        """
        command = step.get('command')
        if not command:
            logger.error("No command found in plan step.")
            return None
        try:
            logger.info(f"Executing command: {command}")
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            logger.info(f"Command output: {result.stdout.strip()}")
            if result.stderr:
                logger.error(f"Command error: {result.stderr.strip()}")
            return result.returncode
        except Exception as e:
            logger.error(f"Dispatch failed: {e}")
            return None 