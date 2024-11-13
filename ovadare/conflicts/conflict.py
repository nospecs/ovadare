# ovadare/conflicts/conflict.py

"""
Conflict Module for the Ovadare Framework

This module provides the Conflict class, which represents a detected conflict
resulting from a policy violation. It includes details about the violation,
the action that caused it, and the agent involved.
"""

import logging
from typing import Dict, Any
from uuid import uuid4

# Configure the logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Conflict:
    """
    Represents a detected conflict resulting from a policy violation.
    """

    def __init__(
        self,
        conflict_id: str = None,
        related_agent_id: str = "",
        action: Dict[str, Any] = None,
        violation_details: str = "",
        policy_id: str = "",
        timestamp: float = None
    ):
        """
        Initializes a Conflict instance.

        Args:
            conflict_id (str, optional): The unique identifier of the conflict.
                If None, a UUID is generated.
            related_agent_id (str): The ID of the agent involved in the conflict.
            action (Dict[str, Any]): The action that caused the conflict.
            violation_details (str): Details about the policy violation.
            policy_id (str): The ID of the policy that was violated.
            timestamp (float, optional): The time the conflict was detected.
        """
        self.conflict_id: str = conflict_id or str(uuid4())
        self.related_agent_id: str = related_agent_id
        self.action: Dict[str, Any] = action or {}
        self.violation_details: str = violation_details
        self.policy_id: str = policy_id
        self.timestamp: float = timestamp or self._current_timestamp()

        logger.debug(f"Conflict '{self.conflict_id}' initialized for agent '{self.related_agent_id}'.")

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializes the Conflict instance to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the conflict.
        """
        conflict_dict = {
            'conflict_id': self.conflict_id,
            'related_agent_id': self.related_agent_id,
            'action': self.action,
            'violation_details': self.violation_details,
            'policy_id': self.policy_id,
            'timestamp': self.timestamp
        }
        logger.debug(f"Conflict '{self.conflict_id}' serialized to dict.")
        return conflict_dict

    @staticmethod
    def _current_timestamp() -> float:
        """
        Gets the current timestamp.

        Returns:
            float: The current time in seconds since the epoch.
        """
        import time
        return time.time()
