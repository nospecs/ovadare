# ovadare/utils/secrets_manager.py

"""
Secrets Manager Module for the Ovadare Framework

This module provides the SecretsManager class, which securely manages sensitive
information like API keys, passwords, and encryption keys. It uses environment
variables and, optionally, encrypted files to store secrets securely.
"""

import logging
import os
from typing import Optional
from cryptography.fernet import Fernet

# Configure the logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SecretsManager:
    """
    Manages secrets securely using environment variables and encryption.
    """

    def __init__(self, encryption_key: Optional[bytes] = None) -> None:
        """
        Initializes the SecretsManager.

        Args:
            encryption_key (Optional[bytes]): The key used for encryption and decryption.
                If None, it attempts to load from the 'SECRETS_ENCRYPTION_KEY' environment variable.
        """
        if encryption_key:
            self.encryption_key = encryption_key
        else:
            key = os.environ.get('SECRETS_ENCRYPTION_KEY')
            if not key:
                logger.error("Encryption key not found in environment variables.")
                raise ValueError("Encryption key is required.")
            self.encryption_key = key.encode('utf-8')
        self.cipher_suite = Fernet(self.encryption_key)
        logger.debug("SecretsManager initialized.")

    def get_secret(self, key: str) -> Optional[str]:
        """
        Retrieves a secret value by its key.

        Args:
            key (str): The key of the secret.

        Returns:
            Optional[str]: The decrypted secret value, or None if not found.
        """
        encrypted_value = os.environ.get(key)
        if encrypted_value:
            try:
                decrypted_value = self.cipher_suite.decrypt(
                    encrypted_value.encode('utf-8')
                ).decode('utf-8')
                logger.debug(f"Secret '{key}' retrieved successfully.")
                return decrypted_value
            except Exception as e:
                logger.error(f"Failed to decrypt secret '{key}': {e}")
                return None
        else:
            logger.warning(f"Secret '{key}' not found.")
            return None

    def set_secret(self, key: str, value: str) -> None:
        """
        Stores a secret value securely.

        Args:
            key (str): The key for the secret.
            value (str): The secret value to store.
        """
        encrypted_value = self.cipher_suite.encrypt(value.encode('utf-8')).decode('utf-8')
        os.environ[key] = encrypted_value
        logger.debug(f"Secret '{key}' stored securely.")

    def generate_encryption_key(self) -> bytes:
        """
        Generates a new encryption key.

        Returns:
            bytes: The generated encryption key.
        """
        key = Fernet.generate_key()
        logger.info("New encryption key generated.")
        return key
