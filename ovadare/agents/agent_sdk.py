# ovadare/agents/agent_sdk.py

"""
Agent SDK Module for the Ovadare Framework

This module provides the AgentSDK class, which allows agents to interact with
the Ovadare Framework. It supports authentication, authorization, action submission,
and feedback submission functionalities.
"""

import logging
import requests
from typing import Optional, Dict, Any

from ovadare.security.authentication import AuthenticationManager
from ovadare.security.authorization import AuthorizationManager

# Configure the logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class AgentSDK:
    """
    Provides methods for agents to interact with the Ovadare Framework.
    """

    def __init__(
        self,
        api_base_url: str,
        authentication_manager: AuthenticationManager,
        authorization_manager: AuthorizationManager
    ) -> None:
        """
        Initializes the AgentSDK.

        Args:
            api_base_url (str): The base URL for the API endpoints.
            authentication_manager (AuthenticationManager): Manages authentication.
            authorization_manager (AuthorizationManager): Manages authorization.
        """
        self.api_base_url = api_base_url
        self.authentication_manager = authentication_manager
        self.authorization_manager = authorization_manager
        self.token: Optional[str] = None
        self.agent_id: Optional[str] = None
        logger.debug("AgentSDK initialized.")

    def register(self, agent_id: str, password: str) -> bool:
        """
        Registers the agent with the framework.

        Args:
            agent_id (str): The unique ID of the agent.
            password (str): The password for the agent.

        Returns:
            bool: True if registration is successful, False otherwise.
        """
        url = f"{self.api_base_url}/register"
        data = {'user_id': agent_id, 'password': password}
        response = requests.post(url, json=data)
        if response.status_code == 201:
            self.agent_id = agent_id
            logger.info(f"Agent '{agent_id}' registered successfully.")
            return True
        else:
            logger.error(f"Registration failed: {response.text}")
            return False

    def login(self, agent_id: str, password: str) -> bool:
        """
        Authenticates the agent and obtains an authentication token.

        Args:
            agent_id (str): The unique ID of the agent.
            password (str): The password for the agent.

        Returns:
            bool: True if login is successful, False otherwise.
        """
        url = f"{self.api_base_url}/login"
        data = {'user_id': agent_id, 'password': password}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            self.token = response.json().get('token')
            self.agent_id = agent_id
            logger.info(f"Agent '{agent_id}' logged in successfully.")
            return True
        else:
            logger.error(f"Login failed: {response.text}")
            return False

    def submit_action(self, action: Dict[str, Any]) -> bool:
        """
        Submits an action to the framework.

        Args:
            action (Dict[str, Any]): The action data.

        Returns:
            bool: True if submission is successful, False otherwise.
        """
        if not self.token or not self.agent_id:
            logger.error("Agent is not authenticated.")
            return False

        url = f"{self.api_base_url}/submit_action"
        headers = {'Authorization': self.token}
        data = {'agent_id': self.agent_id, 'action': action}
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            logger.info(f"Action submitted successfully: {action}")
            return True
        else:
            logger.error(f"Action submission failed: {response.text}")
            return False

    def submit_feedback(
        self,
        feedback_type: str,
        message: str
    ) -> bool:
        """
        Submits feedback to the framework.

        Args:
            feedback_type (str): The type of feedback.
            message (str): The feedback message.

        Returns:
            bool: True if submission is successful, False otherwise.
        """
        if not self.token or not self.agent_id:
            logger.error("Agent is not authenticated.")
            return False

        url = f"{self.api_base_url}/submit_feedback"
        headers = {'Authorization': self.token}
        data = {
            'agent_id': self.agent_id,
            'feedback_type': feedback_type,
            'message': message
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            logger.info(f"Feedback submitted successfully: {message}")
            return True
        else:
            logger.error(f"Feedback submission failed: {response.text}")
            return False

    def logout(self) -> None:
        """
        Logs out the agent by clearing the authentication token.
        """
        logger.info(f"Agent '{self.agent_id}' logged out.")
        self.token = None
        self.agent_id = None
