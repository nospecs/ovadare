# ovadare/core/framework.py

"""
Ovadare Framework Core Module

This module provides the OvadareFramework class, which serves as the central
orchestrator for the Ovadare system. It initializes and manages the core components,
including the AgentRegistry, EventDispatcher, PolicyManager, ConflictDetector,
ResolutionEngine, MonitoringService, APIEndpoints, FeedbackManager, EscalationManager,
AuthenticationManager, and AuthorizationManager.
"""

import logging
from typing import Optional, Dict, Any

from ovadare.core.event_dispatcher import EventDispatcher
from ovadare.agents.agent_registry import AgentRegistry
from ovadare.agents.agent_sdk import AgentSDK
from ovadare.policies.policy_manager import PolicyManager
from ovadare.conflicts.conflict_detector import ConflictDetector
from ovadare.conflicts.resolution_engine import ResolutionEngine
from ovadare.monitoring.monitoring_service import MonitoringService
from ovadare.communication.api_endpoints import APIEndpoints
from ovadare.utils.configuration import Configuration
from ovadare.feedback.feedback_manager import FeedbackManager
from ovadare.escalation.escalation_manager import EscalationManager
from ovadare.security.authentication import AuthenticationManager
from ovadare.security.authorization import AuthorizationManager

# Configure the logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class OvadareFramework:
    """
    The OvadareFramework class initializes and manages the core components of the system.
    It provides methods to start and stop the framework and ensures that all components
    are properly integrated.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
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
        self.feedback_manager = FeedbackManager()
        self.policy_manager = PolicyManager()
        self.conflict_detector = ConflictDetector(policy_manager=self.policy_manager)
        self.resolution_engine = ResolutionEngine()
        self.escalation_manager = EscalationManager()
        self.authentication_manager = AuthenticationManager()
        self.authorization_manager = AuthorizationManager()
        self.monitoring_service = MonitoringService(
            agent_registry=self.agent_registry,
            conflict_detector=self.conflict_detector
        )
        self.api_endpoints = APIEndpoints(
            agent_registry=self.agent_registry,
            event_dispatcher=self.event_dispatcher,
            authentication_manager=self.authentication_manager,
            authorization_manager=self.authorization_manager
        )
        self.agent_sdk = AgentSDK(
            agent_registry=self.agent_registry,
            event_dispatcher=self.event_dispatcher,
            feedback_manager=self.feedback_manager,
            authentication_manager=self.authentication_manager,
            authorization_manager=self.authorization_manager
        )

        logger.debug("Core components initialized.")

        # Register event listeners
        self._register_event_listeners()
        logger.debug("Event listeners registered.")

    def _register_event_listeners(self) -> None:
        """
        Registers event listeners for handling agent actions, conflicts, and resolutions.
        """
        self.event_dispatcher.add_listener('agent_action', self._handle_agent_action)
        self.event_dispatcher.add_listener('conflict_detected', self._handle_conflict_detected)
        self.event_dispatcher.add_listener('resolution_failed', self._handle_resolution_failed)
        self.event_dispatcher.add_listener('feedback_submitted', self._handle_feedback_submitted)
        logger.debug("Event listeners for 'agent_action', 'conflict_detected', 'resolution_failed', and 'feedback_submitted' added.")

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

    def _handle_resolution_failed(self, event_data: Dict[str, Any]) -> None:
        """
        Handles resolution failure events by escalating conflicts.

        Args:
            event_data (Dict[str, Any]): The event data containing the conflict.
        """
        conflict = event_data.get('conflict')
        logger.debug(f"Handling resolution failure for conflict: {conflict}")

        if not conflict:
            logger.error("No conflict provided in event data.")
            return

        self.escalation_manager.escalate_conflict(conflict)

    def _handle_feedback_submitted(self, event_data: Dict[str, Any]) -> None:
        """
        Handles feedback submitted events by processing the feedback.

        Args:
            event_data (Dict[str, Any]): The event data containing feedback details.
        """
        agent_id = event_data.get('agent_id')
        feedback_type = event_data.get('feedback_type')
        message = event_data.get('message')
        logger.debug(f"Handling feedback from agent '{agent_id}': {message}")

        if not agent_id or not feedback_type or not message:
            logger.error("Invalid feedback data.")
            return

        feedback_data = {
            'agent_id': agent_id,
            'feedback_type': feedback_type,
            'message': message,
            'timestamp': self._current_timestamp()
        }
        self.feedback_manager.submit_feedback(feedback_data)

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

    @staticmethod
    def _current_timestamp() -> float:
        """
        Gets the current timestamp.

        Returns:
            float: The current time in seconds since the epoch.
        """
        import time
        return time.time()
