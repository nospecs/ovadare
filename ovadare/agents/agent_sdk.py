# ovadare/agents/agent_sdk.py

"""
Agent SDK Module for the Ovadare Framework

This module provides the AgentSDK class, which offers utilities and interfaces
for agents to interact with the Ovadare framework. It includes methods for
registering agents, submitting actions, receiving resolutions, and providing feedback.
"""

import logging
from typing import Dict, Any

from ovadare.agents.agent_interface import AgentInterface
from ovadare.agents.agent_registry import AgentRegistry
from ovadare.core.event_dispatcher import EventDispatcher
from ovadare.feedback.feedback_manager import FeedbackManager

# Configure the logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class AgentSDK:
    """
    Provides utilities for agents to interact with the Ovadare framework.
    """

    def __init__(
        self,
        agent_registry: AgentRegistry,
        event_dispatcher: EventDispatcher,
        feedback_manager: FeedbackManager
    ) -> None:
        """
        Initializes the AgentSDK.

        Args:
            agent_registry (AgentRegistry): The registry for managing agents.
            event_dispatcher (EventDispatcher): The event dispatcher for sending events.
            feedback_manager (FeedbackManager): The feedback manager for submitting feedback.
        """
        self.agent_registry = agent_registry
        self.event_dispatcher = event_dispatcher
        self.feedback_manager = feedback_manager
        logger.debug("AgentSDK initialized.")

    def register_agent(self, agent: AgentInterface) -> None:
        """
        Registers an agent with the framework.

        Args:
            agent (AgentInterface): The agent to register.
        """
        self.agent_registry.register_agent(agent)
        logger.info(f"Agent '{agent.agent_id}' registered successfully.")

    def submit_action(self, agent_id: str, action: Dict[str, Any]) -> None:
        """
        Submits an action performed by an agent to the framework.

        Args:
            agent_id (str): The ID of the agent performing the action.
            action (Dict[str, Any]): The action data.
        """
        event_data = {'agent_id': agent_id, 'action': action}
        logger.debug(f"Agent '{agent_id}' submitting action: {action}")
        self.event_dispatcher.dispatch('agent_action', event_data)

    def submit_feedback(self, agent_id: str, feedback_type: str, message: str) -> None:
        """
        Submits feedback from an agent to the framework.

        Args:
            agent_id (str): The ID of the agent submitting feedback.
            feedback_type (str): The type of feedback (e.g., 'policy_issue', 'system_error').
            message (str): The feedback message.
        """
        feedback_data = {
            'agent_id': agent_id,
            'feedback_type': feedback_type,
            'message': message,
            'timestamp': self._current_timestamp()
        }
        logger.debug(f"Agent '{agent_id}' submitting feedback: {feedback_data}")
        try:
            self.feedback_manager.submit_feedback(feedback_data)
            logger.info(f"Feedback from agent '{agent_id}' submitted successfully.")
        except ValueError as e:
            logger.error(f"Error submitting feedback from agent '{agent_id}': {e}")

    def receive_resolutions(self, agent_id: str) -> None:
        """
        Placeholder method for agents to receive resolutions sent by the framework.

        Args:
            agent_id (str): The ID of the agent.
        """
        # This method would include logic for the agent to receive resolutions
        # from the framework. Implementation depends on the communication mechanisms.
        logger.debug(f"Agent '{agent_id}' checking for resolutions.")
        # Placeholder implementation
        pass

    @staticmethod
    def _current_timestamp() -> float:
        """
        Gets the current timestamp.

        Returns:
            float: The current time in seconds since the epoch.
        """
        import time
        return time.time()
