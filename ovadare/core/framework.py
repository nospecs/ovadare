# ovadare/core/framework.py

"""
Ovadare Framework Core Module

This module provides the OvadareFramework class, which serves as the central
orchestrator for the Ovadare system. It initializes and manages the core components,
including the AgentRegistry, EventDispatcher, PolicyManager, ConflictDetector,
ResolutionEngine, MonitoringService, and APIEndpoints.
"""

import logging
from typing import Optional, Dict, Any

from ovadare.core.event_dispatcher import EventDispatcher
from ovadare.agents.agent_registry import AgentRegistry
from ovadare.policies.policy_manager import PolicyManager
from ovadare.conflicts.conflict_detector import ConflictDetector
from ovadare.conflicts.resolution_engine import ResolutionEngine
from ovadare.monitoring.monitoring_service import MonitoringService
from ovadare.communication.api_endpoints import APIEndpoints
from ovadare.utils.configuration import Configuration

# Configure the logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class OvadareFramework:
    """
    The OvadareFramework class initializes and manages the core components of the system.
    It provides methods to start and stop the framework and ensures that all components
    are properly integrated.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initializes the Ovadare Framework.

        Args:
            config (Optional[Dict[str, Any]]): Configuration settings for the framework.
                If None, the default configuration is loaded.
        """
        logger.info("Initializing Ovadare Framework...")

        # Load configuration
        if config:
            Configuration._config = config
        else:
            Configuration.load_default()
        self.config = Configuration.get_all()
        logger.debug(f"Configuration loaded: {self.config}")

        # Initialize core components
        self.event_dispatcher = EventDispatcher()
        self.agent_registry = AgentRegistry()
        self.policy_manager = PolicyManager()
        self.conflict_detector = ConflictDetector(policy_manager=self.policy_manager)
        self.resolution_engine = ResolutionEngine(agent_registry=self.agent_registry)
        self.monitoring_service = MonitoringService(
            agent_registry=self.agent_registry,
            conflict_detector=self.conflict_detector
        )
        self.api_endpoints = APIEndpoints(
            agent_registry=self.agent_registry,
            event_dispatcher=self.event_dispatcher
        )

        logger.debug("Core components initialized.")

        # Register event listeners
        self._register_event_listeners()
        logger.debug("Event listeners registered.")

    def _register_event_listeners(self) -> None:
        """
        Registers event listeners for handling agent actions and conflicts.
        """
        self.event_dispatcher.add_listener('agent_action', self._handle_agent_action)
        self.event_dispatcher.add_listener('conflict_detected', self._handle_conflict_detected)
        logger.debug("Event listeners for 'agent_action' and 'conflict_detected' added.")

    def _handle_agent_action(self, event_data: Dict[str, Any]) -> None:
        """
        Handles agent action events by detecting conflicts.

        Args:
            event_data (Dict[str, Any]): The event data containing agent ID and action.
        """
        agent_id = event_data.get('agent_id')
        action = event_data.get('action')
        logger.debug(f"Handling agent action for agent '{agent_id}': {action}")

        if not agent_id or not action:
            logger.error("Invalid event data: 'agent_id' and 'action' are required.")
            return

        conflicts = self.conflict_detector.detect(agent_id, action)
        if conflicts:
            logger.info(f"Conflicts detected for agent '{agent_id}': {conflicts}")
            self.event_dispatcher.dispatch('conflict_detected', {'conflicts': conflicts})

    def _handle_conflict_detected(self, event_data: Dict[str, Any]) -> None:
        """
        Handles conflict detected events by generating and applying resolutions.

        Args:
            event_data (Dict[str, Any]): The event data containing conflicts.
        """
        conflicts = event_data.get('conflicts', [])
        logger.debug(f"Handling conflicts: {conflicts}")

        if not conflicts:
            logger.error("No conflicts provided in event data.")
            return

        resolutions = self.resolution_engine.generate_resolutions(conflicts)
        self.resolution_engine.apply_resolutions(resolutions)

    def start(self) -> None:
        """
        Starts the Ovadare Framework, including the API server and monitoring service.
        """
        logger.info("Starting Ovadare Framework...")

        # Start the monitoring service
        self.monitoring_service.start()
        logger.debug("Monitoring service started.")

        # Start the API server
        host = Configuration.get('api_host', '0.0.0.0')
        port = Configuration.get('api_port', 5000)
        logger.debug(f"Starting API server on {host}:{port}.")
        self.api_endpoints.start(host=host, port=port)

        logger.info("Ovadare Framework started.")

    def stop(self) -> None:
        """
        Stops the Ovadare Framework, including the API server and monitoring service.
        """
        logger.info("Stopping Ovadare Framework...")

        # Stop the monitoring service
        self.monitoring_service.stop()
        logger.debug("Monitoring service stopped.")

        # Stop the API server
        self.api_endpoints.stop()
        logger.debug("API server stopped.")

        logger.info("Ovadare Framework stopped.")