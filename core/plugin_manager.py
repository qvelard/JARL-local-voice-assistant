"""
Plugin manager module for skill discovery and loading.
"""
from typing import List, Any
import os
import importlib.util
from core.utils import logger, load_config

class PluginManager:
    """
    Discovers and loads skills from services/skills.
    """
    def __init__(self) -> None:
        self.config = load_config()
        self.skills_dir = os.path.join(os.path.dirname(__file__), 'skills')
        self.skills: List[Any] = []

    def discover_skills(self) -> List[str]:
        """
        Discovers available skill modules.
        """
        try:
            skills = [f[:-3] for f in os.listdir(self.skills_dir) if f.endswith('.py') and not f.startswith('_')]
            logger.info(f"Discovered skills: {skills}")
            return skills
        except Exception as e:
            logger.error(f"Skill discovery failed: {e}")
            return []

    def load_skills(self) -> None:
        """
        Loads and validates skill modules.
        """
        self.skills = []
        for skill_name in self.discover_skills():
            try:
                skill_path = os.path.join(self.skills_dir, f"{skill_name}.py")
                spec = importlib.util.spec_from_file_location(skill_name, skill_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    self.skills.append(module)
                    logger.info(f"Loaded skill: {skill_name}")
            except Exception as e:
                logger.error(f"Failed to load skill {skill_name}: {e}") 