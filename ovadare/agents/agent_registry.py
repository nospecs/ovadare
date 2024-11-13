# ovadare/agents/agent_registry.py

"""
Agent Registry Module for the Ovadare Framework

This module provides the AgentRegistry class, which is responsible for managing
the registration, retrieval, and lifecycle of agents within the framework.
"""

from typing import Dict, List, Optional
from threading import Lock
import logging

from ovadare.agents.agent_interface import AgentInterface

# Configure the logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class AgentRegistry:
    """
    The AgentRegistry manages the agents registered within the Ovadare framework.
    It allows for registering new agents, retrieving existing agents, and unregistering agents.
    """

    _instance = None
    _lock = Lock()

    def __new__(cls):
        """
        Implements the Singleton pattern to ensure only one instance of AgentRegistry exists.
        """
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(AgentRegistry, cls).__new__(cls)
                    cls._instance._agents = {}
                    cls._instance._agents_lock = Lock()
                    logger.debug("Created a new instance of AgentRegistry.")
        return cls._instance

    def register_agent(self, agent: AgentInterface) -> None:
        """
        Registers an agent with the registry.

        Args:
            agent (AgentInterface): The agent to register.

        Raises:
            ValueError: If an agent with the same ID is already registered.
        """
        with self._agents_lock:
            if agent.agent_id in self._agents:
                error_message = f"Agent with ID '{agent.agent_id}' is already registered."
                logger.error(error_message)
                raise ValueError(error_message)
            else:
                self._agents[agent.agent_id] = agent
                logger.debug(f"Agent '{agent.agent_id}' registered successfully.")
                agent.initialize()

    def unregister_agent(self, agent_id: str) -> None:
        """
        Unregisters an agent from the registry.

        Args:
            agent_id (str): The ID of the agent to unregister.

        Raises:
            ValueError: If the agent is not found in the registry.
        """
        with self._agents_lock:
            if agent_id in self._agents:
                agent = self._agents.pop(agent_id)
                agent.shutdown()
                logger.debug(f"Agent '{agent_id}' unregistered successfully.")
            else:
                error_message = f"Agent with ID '{agent_id}' not found."
                logger.error(error_message)
                raise ValueError(error_message)

    def get_agent(self, agent_id: str) -> Optional[AgentInterface]:
        """
        Retrieves an agent by its ID.

        Args:
            agent_id (str): The ID of the agent to retrieve.

        Returns:
            Optional[AgentInterface]: The agent if found, else None.
        """
        with self._agents_lock:
            agent = self._agents.get(agent_id)
            if agent:
                logger.debug(f"Retrieved agent '{agent_id}'.")
            else:
                logger.warning(f"Agent '{agent_id}' not found.")
            return agent

    def get_all_agents(self) -> List[AgentInterface]:
        """
        Retrieves a list of all registered agents.

        Returns:
            List[AgentInterface]: A list of all registered agents.
        """
        with self._agents_lock:
            agents_list = list(self._agents.values())
            logger.debug(f"Retrieved all agents. Total count: {len(agents_list)}.")
            return agents_list

    def find_agents_by_capability(self, capability: str) -> List[AgentInterface]:
        """
        Finds agents that have a specific capability.

        Args:
            capability (str): The capability to search for.

        Returns:
            List[AgentInterface]: A list of agents that have the specified capability.
        """
        with self._agents_lock:
            agents_with_capability = [agent for agent in self._agents.values() if capability in agent.capabilities]
            logger.debug(f"Found {len(agents_with_capability)} agent(s) with capability '{capability}'.")
            return agents_with_capability
