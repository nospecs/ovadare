# ovadare/communication/api_endpoints.py

"""
API Endpoints Module for the Ovadare Framework

This module provides the APIEndpoints class, which sets up RESTful API endpoints
for communication with external agents and systems. It allows agents to register,
submit actions, and receive updates, facilitating interaction with the framework.
"""

from typing import Optional, Dict, Any
import logging
import threading

from flask import Flask, request, jsonify
from werkzeug.serving import make_server

from ovadare.agents.agent_interface import AgentInterface
from ovadare.agents.agent_registry import AgentRegistry
from ovadare.core.event_dispatcher import EventDispatcher

# Configure the logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class APIEndpoints:
    """
    The APIEndpoints class sets up RESTful API endpoints for communication
    with external agents and systems.
    """

    def __init__(
        self,
        agent_registry: Optional[AgentRegistry] = None,
        event_dispatcher: Optional[EventDispatcher] = None,
        host: str = '0.0.0.0',
        port: int = 5000
    ):
        """
        Initializes the APIEndpoints.

        Args:
            agent_registry (Optional[AgentRegistry]): An instance of AgentRegistry.
                If None, a new AgentRegistry is instantiated.
            event_dispatcher (Optional[EventDispatcher]): An instance of EventDispatcher.
                If None, a new EventDispatcher is instantiated.
            host (str): The host address to bind the server to.
            port (int): The port number to listen on.
        """
        self.agent_registry = agent_registry or AgentRegistry()
        self.event_dispatcher = event_dispatcher or EventDispatcher()
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self.server = None
        self.thread = None
        self._setup_routes()
        logger.debug("APIEndpoints initialized.")

    def _setup_routes(self):
        """
        Sets up the API routes for agent registration, action submission, etc.
        """

        @self.app.route('/register_agent', methods=['POST'])
        def register_agent():
            data = request.get_json()
            if not data:
                logger.error("No JSON data received in /register_agent")
                return jsonify({'error': 'Invalid JSON data'}), 400

            agent_id = data.get('agent_id')
            capabilities = data.get('capabilities', [])
            if not agent_id:
                logger.error("agent_id is missing in /register_agent request")
                return jsonify({'error': 'agent_id is required'}), 400

            # Create an agent instance
            agent = self._create_agent(agent_id, capabilities)
            try:
                self.agent_registry.register_agent(agent)
                logger.info(f"Agent '{agent_id}' registered successfully.")
                return jsonify({'message': f'Agent {agent_id} registered successfully.'}), 200
            except ValueError as e:
                logger.error(f"Error registering agent '{agent_id}': {e}")
                return jsonify({'error': str(e)}), 400

        @self.app.route('/submit_action', methods=['POST'])
        def submit_action():
            data = request.get_json()
            if not data:
                logger.error("No JSON data received in /submit_action")
                return jsonify({'error': 'Invalid JSON data'}), 400

            agent_id = data.get('agent_id')
            action = data.get('action')
            if not agent_id or not action:
                logger.error("agent_id or action is missing in /submit_action request")
                return jsonify({'error': 'agent_id and action are required'}), 400

            agent = self.agent_registry.get_agent(agent_id)
            if not agent:
                logger.error(f"Agent '{agent_id}' not found in /submit_action")
                return jsonify({'error': f'Agent {agent_id} not found'}), 404

            # Dispatch an event for the agent action
            self.event_dispatcher.dispatch_event('agent_action', agent_id=agent_id, action=action)
            logger.info(f"Action submitted by agent '{agent_id}'")
            return jsonify({'message': 'Action submitted successfully.'}), 200

        @self.app.route('/unregister_agent', methods=['POST'])
        def unregister_agent():
            data = request.get_json()
            if not data:
                logger.error("No JSON data received in /unregister_agent")
                return jsonify({'error': 'Invalid JSON data'}), 400

            agent_id = data.get('agent_id')
            if not agent_id:
                logger.error("agent_id is missing in /unregister_agent request")
                return jsonify({'error': 'agent_id is required'}), 400

            try:
                self.agent_registry.unregister_agent(agent_id)
                logger.info(f"Agent '{agent_id}' unregistered successfully.")
                return jsonify({'message': f'Agent {agent_id} unregistered successfully.'}), 200
            except ValueError as e:
                logger.error(f"Error unregistering agent '{agent_id}': {e}")
                return jsonify({'error': str(e)}), 400

        logger.debug("API routes set up.")

    def _create_agent(self, agent_id: str, capabilities: list) -> AgentInterface:
        """
        Creates an agent instance based on the provided agent ID and capabilities.

        Args:
            agent_id (str): The ID of the agent.
            capabilities (list): A list of capabilities for the agent.

        Returns:
            AgentInterface: The created agent instance.
        """
        # For demonstration, we'll create a simple agent that implements AgentInterface
        class ExternalAgent(AgentInterface):
            def __init__(self, agent_id: str, capabilities: list):
                self._agent_id = agent_id
                self._capabilities = capabilities
                self.logger = logging.getLogger(__name__)

            @property
            def agent_id(self) -> str:
                return self._agent_id

            @property
            def capabilities(self) -> list:
                return self._capabilities

            def initialize(self) -> None:
                self.logger.debug(f"Initializing agent '{self.agent_id}'.")

            def shutdown(self) -> None:
                self.logger.debug(f"Shutting down agent '{self.agent_id}'.")

            def perform_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
                # Implementation omitted for brevity
                return {}

            def report_status(self) -> Dict[str, Any]:
                return {'status': 'active'}

            def handle_event(self, event_type: str, event_data: Dict[str, Any]) -> None:
                self.logger.debug(f"Agent '{self.agent_id}' received event '{event_type}' with data: {event_data}")

            def handle_resolution(self, resolution: Any) -> None:
                self.logger.debug(f"Agent '{self.agent_id}' received resolution: {resolution}")

        return ExternalAgent(agent_id, capabilities)

    def start(self):
        """
        Starts the API server in a separate thread.
        """
        logger.info(f"Starting API server on {self.host}:{self.port}...")
        self.server = make_server(self.host, self.port, self.app)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()
        logger.info("API server started.")

    def stop(self):
        """
        Stops the API server.
        """
        if self.server:
            logger.info("Stopping API server...")
            self.server.shutdown()
            self.thread.join()
            logger.info("API server stopped.")
