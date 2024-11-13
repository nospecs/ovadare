# ovadare/agents/agent_interface.py

"""
Agent Interface Module for the Ovadare Framework

This module provides the AgentInterface, which defines the methods that agents must
implement to interact with the Ovadare framework. Agents represent entities that perform
actions within the system and may need to respond to resolutions for conflicts.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
import logging

from ovadare.conflicts.resolution import Resolution

# Configure the logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class AgentInterface(ABC):
    """
    Abstract base class for agents in the Ovadare framework.
    Agents must implement this interface to interact with the framework.
    """

    @property
    @abstractmethod
    def agent_id(self) -> str:
        """
        Returns the unique identifier of the agent.

        Returns:
            str: The agent's unique ID.
        """
        pass

    @property
    @abstractmethod
    def capabilities(self) -> Dict[str, Any]:
        """
        Returns the capabilities of the agent.

        Returns:
            Dict[str, Any]: A dictionary representing the agent's capabilities.
        """
        pass

    @abstractmethod
    def initialize(self) -> None:
        """
        Initializes the agent. Called when the agent is registered with the framework.
        """
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """
        Shuts down the agent. Called when the agent is unregistered from the framework.
        """
        pass

    @abstractmethod
    def perform_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Performs an action.

        Args:
            action (Dict[str, Any]): A dictionary representing the action to perform.

        Returns:
            Dict[str, Any]: The result of the action.
        """
        pass

    @abstractmethod
    def report_status(self) -> Dict[str, Any]:
        """
        Reports the current status of the agent.

        Returns:
            Dict[str, Any]: A dictionary representing the agent's status.
        """
        pass

    @abstractmethod
    def handle_event(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """
        Handles an event dispatched by the framework.

        Args:
            event_type (str): The type of event.
            event_data (Dict[str, Any]): The data associated with the event.
        """
        pass

    @abstractmethod
    def handle_resolution(self, resolution: Resolution) -> None:
        """
        Handles a resolution provided by the ResolutionEngine in response to a conflict.

        Args:
            resolution (Resolution): The resolution to apply.
        """
        pass
