"""
Utils module: config loader, structured logger, JSON schema loader.
"""
from typing import Any, Dict
import logging
import yaml
import os
import json

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configs', 'config.yaml')

# Structured logger
logger = logging.getLogger('voice_assistant')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(name)s: %(message)s')
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)


def load_config() -> Dict[str, Any]:
    """
    Loads YAML config from configs/config.yaml.
    """
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        logger.info("Config loaded successfully.")
        return config or {}
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        return {}

def load_json_schema(path: str) -> Dict[str, Any]:
    """
    Loads a JSON schema from file.
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        logger.info(f"Loaded JSON schema: {path}")
        return schema
    except Exception as e:
        logger.error(f"Failed to load JSON schema {path}: {e}")
        return {} 