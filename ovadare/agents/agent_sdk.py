# ovadare/agents/agent_sdk.py

"""
Agent SDK Module

This module provides a Software Development Kit (SDK) for developers to create
agents that integrate with the Ovadare framework. The SDK offers a base class
'BaseAgent' that implements the 'AgentInterface' and handles communication
with the framework, allowing developers to focus on agent-specific logic.
"""

from ovadare.core.base_classes import AgentInterface, Resolution
from ovadare.utils.logger import Logger
from ovadare.core.event_dispatcher import EventDispatcher
from typing import List, Dict, Any, Optional


class BaseAgent(AgentInterface):
    """
    Base class for agents integrating with the Ovadare framework.
    Implements the AgentInterface and provides common functionalities.
    """

    def __init__(self, agent_id: str, capabilities: List[str], event_dispatcher: EventDispatcher):
        """
        Initializes the BaseAgent.

        Args:
            agent_id (str): Unique identifier for the agent.
            capabilities (List[str]): List of actions or tasks the agent can perform.
            event_dispatcher (EventDispatcher): Event dispatcher instance for communication.

        Raises:
            ValueError: If 'agent_id' is invalid or empty.
            TypeError: If 'capabilities' is not a list of strings.
        """
        if not agent_id:
            raise ValueError("agent_id must be a valid non-empty string.")
        if not isinstance(capabilities, list) or not all(isinstance(cap, str) for cap in capabilities):
            raise TypeError("capabilities must be a list of strings.")
        if not isinstance(event_dispatcher, EventDispatcher):
            raise TypeError("event_dispatcher must be an instance of EventDispatcher.")

        self._agent_id = agent_id
        self._capabilities = capabilities
        self._event_dispatcher = event_dispatcher
        self.logger = Logger(f"Agent-{self._agent_id}")
        self.logger.debug(f"Agent '{self._agent_id}' initialized with capabilities: {self._capabilities}")

    @property
    def agent_id(self) -> str:
        """Unique identifier for the agent."""
        return self._agent_id

    @property
    def capabilities(self) -> List[str]:
        """List of actions or tasks the agent can perform."""
        return self._capabilities

    def report_action(self, action: Dict[str, Any]) -> None:
        """
        Reports an action that the agent intends to perform to the framework.

        Args:
            action (Dict[str, Any]): The action to be reported.

        Raises:
            ValueError: If 'action' is not a valid dictionary.
        """
        if not isinstance(action, dict):
            self.logger.error("Invalid action format. 'action' must be a dictionary.")
            raise ValueError("action must be a dictionary.")

        self.logger.debug(f"Agent '{self._agent_id}' reporting action: {action}")
        event_data = {
            'agent_id': self._agent_id,
            'action': action
        }
        try:
            self._event_dispatcher.dispatch('agent_action', event_data)
            self.logger.debug(f"Action reported successfully: {action}")
        except Exception as e:
            self.logger.error(f"Failed to report action: {e}")
            raise

    def receive_resolution(self, resolution: Resolution) -> None:
        """
        Receives a resolution from the framework.

        Args:
            resolution (Resolution): The resolution to be applied.

        Raises:
            ValueError: If 'resolution' is not an instance of Resolution.
        """
        if not isinstance(resolution, Resolution):
            self.logger.error("Invalid resolution received. Must be an instance of Resolution.")
            raise ValueError("resolution must be an instance of Resolution.")

        self.logger.info(f"Agent '{self._agent_id}' received resolution: {resolution.explanation}")
        # Apply the resolution's actions
        self.apply_resolution(resolution)

    def apply_resolution(self, resolution: Resolution) -> None:
        """
        Applies the resolution's actions. Override this method to define custom behavior.

        Args:
            resolution (Resolution): The resolution to apply.
        """
        self.logger.debug(f"Agent '{self._agent_id}' applying resolution actions.")
        # Default implementation: Log the actions
        for action in resolution.actions:
            self.logger.info(f"Executing action: {action}")
            # Implement default action handling logic if necessary

    def perform_task(self, task_data: Dict[str, Any]) -> None:
        """
        Performs a task specific to the agent. Override this method with agent-specific logic.

        Args:
            task_data (Dict[str, Any]): Data related to the task to be performed.
        """
        self.logger.debug(f"Agent '{self._agent_id}' performing task: {task_data}")
        # Agent-specific task implementation goes here
        raise NotImplementedError("perform_task must be implemented by the subclass.")

    def update_capabilities(self, new_capabilities: List[str]) -> None:
        """
        Updates the agent's capabilities.

        Args:
            new_capabilities (List[str]): The new list of capabilities.

        Raises:
            TypeError: If 'new_capabilities' is not a list of strings.
        """
        if not isinstance(new_capabilities, list) or not all(isinstance(cap, str) for cap in new_capabilities):
            self.logger.error("Invalid capabilities format. Must be a list of strings.")
            raise TypeError("new_capabilities must be a list of strings.")

        self._capabilities = new_capabilities
        self.logger.info(f"Agent '{self._agent_id}' updated capabilities: {self._capabilities}")

    def shutdown(self) -> None:
        """
        Shuts down the agent and performs any necessary cleanup.
        """
        self.logger.info(f"Agent '{self._agent_id}' is shutting down.")
        # Implement cleanup logic if necessary

    # Additional helper methods can be added here to support agent functionality
