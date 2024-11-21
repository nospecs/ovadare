# ovadare/utils/configuration.py

"""
Configuration Module for the Ovadare Framework

This module provides the Configuration class, which manages configuration
settings for the framework. It supports loading configurations from environment
variables, JSON files, and default settings.
"""

import logging
import os
import json
from typing import Any, Dict, Optional

# Configure the logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Configuration:
    """
    Manages configuration settings for the Ovadare Framework.
    """
    _config: Dict[str, Any] = {}
    _default_config: Dict[str, Any] = {
        'api_host': '0.0.0.0',
        'api_port': 5000,
        'api_base_url': 'http://localhost:5000',
        'conflict_storage_file': 'conflicts_data.json',
        'resolution_storage_file': 'resolutions_data.json',
        'logging_level': 'INFO',
        'config_file_path': 'config.json',
    }

    @classmethod
    def load(cls, config_file_path: Optional[str] = None) -> None:
        """
        Loads configuration settings from a JSON file, environment variables,
        and merges them with default settings.

        Args:
            config_file_path (Optional[str]): Path to the configuration file.
                If None, uses the default path specified in the default configuration.
        """
        # Start with default configuration
        cls._config = cls._default_config.copy()
        logger.debug("Default configuration loaded.")

        # Load configuration from file
        file_path = config_file_path or cls._config.get('config_file_path')
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
                    cls._config.update(file_config)
                logger.debug(f"Configuration loaded from file '{file_path}'.")
            except Exception as e:
                logger.error(f"Failed to load configuration file '{file_path}': {e}")
        else:
            logger.warning(f"Configuration file '{file_path}' not found. Using defaults and environment variables.")

        # Override with environment variables
        for key in cls._config.keys():
            env_value = os.environ.get(key.upper())
            if env_value is not None:
                cls._config[key] = env_value
                logger.debug(f"Configuration '{key}' set from environment variable.")

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """
        Retrieves a configuration value by key.

        Args:
            key (str): The configuration key.
            default (Any): The default value if the key is not found.

        Returns:
            Any: The configuration value.
        """
        return cls._config.get(key, default)

    @classmethod
    def set(cls, key: str, value: Any) -> None:
        """
        Sets a configuration value.

        Args:
            key (str): The configuration key.
            value (Any): The value to set.
        """
        cls._config[key] = value
        logger.debug(f"Configuration '{key}' set to '{value}'.")

    @classmethod
    def get_all(cls) -> Dict[str, Any]:
        """
        Retrieves all configuration settings.

        Returns:
            Dict[str, Any]: All configuration settings.
        """
        return cls._config.copy()
