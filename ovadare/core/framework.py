# ovadare/core/framework.py

"""
Ovadare Framework Core Module

This module provides the OvadareFramework class, which serves as the central
orchestrator for the Ovadare system. It initializes and manages the core components,
including the AgentRegistry, EventDispatcher, PolicyManager, ConflictDetector,
ResolutionEngine, MonitoringService, APIEndpoints, FeedbackManager, EscalationManager,
AuthenticationManager, AuthorizationManager, and SecretsManager.
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
from ovadare.utils.secrets_manager import SecretsManager

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

        # Initialize SecretsManager
        self.secrets_manager = SecretsManager()

        # Initialize core components
        self.event_dispatcher = EventDispatcher()
        self.agent_registry = AgentRegistry()
        self.feedback_manager = FeedbackManager()
        self.policy_manager = PolicyManager()
        self.conflict_detector = ConflictDetector(policy_manager=self.policy_manager)
        self.resolution_engine = ResolutionEngine()
        self.authentication_manager = AuthenticationManager()
        self.authorization_manager = AuthorizationManager()
        self.escalation_manager = EscalationManager(secrets_manager=self.secrets_manager)
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
        # Update AgentSDK initialization to remove unnecessary parameters
        self.agent_sdk = AgentSDK(
            api_base_url=Configuration.get('api_base_url', 'http://localhost:5000'),
            authentication_manager=self.authentication_manager,
            authorization_manager=self.authorization_manager
        )

        logger.debug("Core components initialized.")

        # Register event listeners
        self._register_event_listeners()
        logger.debug("Event listeners registered.")

    # Rest of the OvadareFramework class remains unchanged...
