# ovadare/conflicts/resolution.py

"""
Resolution Module for the Ovadare Framework

This module provides the Resolution class, which represents a proposed resolution
for a detected conflict. It includes details about the corrective action to be taken,
the conflict it addresses, and an explanation.
"""

import logging
from typing import Dict, Any, Optional
from uuid import uuid4
import time

# Configure the logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Resolution:
    """
    Represents a proposed resolution for a detected conflict.
    """

    def __init__(
        self,
        resolution_id: Optional[str] = None,
        conflict_id: str = "",
        corrective_action: Optional[Dict[str, Any]] = None,
        explanation: str = "",
        timestamp: Optional[float] = None
    ):
        """
        Initializes a Resolution instance.

        Args:
            resolution_id (Optional[str]): The unique identifier of the resolution.
                If None, a UUID is generated.
            conflict_id (str): The ID of the conflict this resolution addresses.
            corrective_action (Optional[Dict[str, Any]]): The action proposed to resolve the conflict.
            explanation (str): A description or explanation of the resolution.
            timestamp (Optional[float]): The time the resolution was generated.
        """
        self.resolution_id: str = resolution_id or str(uuid4())
        self.conflict_id: str = conflict_id
        self.corrective_action: Dict[str, Any] = corrective_action or {}
        self.explanation: str = explanation
        self.timestamp: float = timestamp or self._current_timestamp()

        logger.debug(
            f"Resolution '{self.resolution_id}' initialized for conflict '{self.conflict_id}'."
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializes the Resolution instance to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the resolution.
        """
        resolution_dict = {
            'resolution_id': self.resolution_id,
            'conflict_id': self.conflict_id,
            'corrective_action': self.corrective_action,
            'explanation': self.explanation,
            'timestamp': self.timestamp
        }
        logger.debug(f"Resolution '{self.resolution_id}' serialized to dict.")
        return resolution_dict

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Resolution':
        """
        Creates a Resolution instance from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing resolution data.

        Returns:
            Resolution: A new Resolution instance.
        """
        resolution = cls(
            resolution_id=data.get('resolution_id'),
            conflict_id=data.get('conflict_id', ""),
            corrective_action=data.get('corrective_action'),
            explanation=data.get('explanation', ""),
            timestamp=data.get('timestamp')
        )
        logger.debug(f"Resolution '{resolution.resolution_id}' created from dict.")
        return resolution

    def __repr__(self) -> str:
        """
        Returns a string representation of the Resolution instance.

        Returns:
            str: A string representation of the resolution.
        """
        return (
            f"Resolution(resolution_id='{self.resolution_id}', conflict_id='{self.conflict_id}', "
            f"corrective_action={self.corrective_action}, explanation='{self.explanation}', "
            f"timestamp={self.timestamp})"
        )

    @staticmethod
    def _current_timestamp() -> float:
        """
        Gets the current timestamp.

        Returns:
            float: The current time in seconds since the epoch.
        """
        return time.time()
