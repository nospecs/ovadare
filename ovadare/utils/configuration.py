# ovadare/utils/configuration.py

"""
Configuration Module for the Ovadare Framework

This module provides the Configuration class, which handles loading and accessing
configuration settings for the framework. It supports loading configurations from
JSON files and environment variables.
"""

import os
import json
import logging
from typing import Any, Dict, Optional
from threading import Lock

# Configure the logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Configuration:
    """
    The Configuration class handles loading and accessing configuration settings
    for the Ovadare framework.
    """

    _config: Dict[str, Any] = {}
    _lock = Lock()

    @classmethod
    def load(cls, config_file: Optional[str] = None) -> None:
        """
        Loads configuration settings from a JSON file and environment variables.

        Args:
            config_file (Optional[str]): The path to the configuration file.
                If None, defaults to 'config.json'.
        """
        config_file = config_file or 'config.json'
        logger.debug(f"Loading configuration from file: '{config_file}'")

        with cls._lock:
            # Load configurations from file
            if os.path.exists(config_file):
                try:
                    with open(config_file, 'r') as f:
                        file_config = json.load(f)
                        if not isinstance(file_config, dict):
                            raise ValueError("Configuration file must contain a JSON object at the root.")
                        cls._config.update(file_config)
                        logger.debug("Configuration loaded from file.")
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decoding error in configuration file '{config_file}': {e}", exc_info=True)
                except Exception as e:
                    logger.error(f"Error reading configuration file '{config_file}': {e}", exc_info=True)
            else:
                logger.warning(f"Configuration file '{config_file}' not found. Using defaults and environment variables.")

            # Override with environment variables
            for key in list(cls._config.keys()):
                env_value = os.getenv(key.upper())
                if env_value is not None:
                    cls._config[key] = cls._parse_env_value(env_value)
                    logger.debug(f"Configuration '{key}' overridden by environment variable.")

    @classmethod
    def load_default(cls) -> None:
        """
        Loads the default configuration settings.
        """
        cls.load()

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """
        Retrieves a configuration value by key.

        Args:
            key (str): The configuration key.
            default (Any): The default value to return if the key is not found.

        Returns:
            Any: The configuration value.
        """
        with cls._lock:
            value = cls._config.get(key, default)
            logger.debug(f"Retrieved configuration '{key}': {value}")
            return value

    @classmethod
    def set(cls, key: str, value: Any) -> None:
        """
        Sets a configuration value.

        Args:
            key (str): The configuration key.
            value (Any): The value to set.
        """
        with cls._lock:
            cls._config[key] = value
            logger.debug(f"Configuration '{key}' set to: {value}")

    @classmethod
    def get_all(cls) -> Dict[str, Any]:
        """
        Retrieves all configuration settings.

        Returns:
            Dict[str, Any]: A dictionary of all configuration settings.
        """
        with cls._lock:
            logger.debug("Retrieving all configuration settings.")
            return cls._config.copy()

    @staticmethod
    def _parse_env_value(value: str) -> Any:
        """
        Parses an environment variable value, attempting to convert it to the appropriate type.

        Args:
            value (str): The environment variable value as a string.

        Returns:
            Any: The parsed value in the appropriate type.
        """
        # Attempt to parse booleans and numbers
        if value.lower() in {'true', 'false'}:
            return value.lower() == 'true'
        try:
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            # Return the string value if it cannot be converted
            return value
