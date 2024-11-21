# ovadare/communication/api_endpoints.py

"""
API Endpoints Module for the Ovadare Framework

This module provides the APIEndpoints class, which defines RESTful API endpoints
for agents and users to interact with the framework. It integrates authentication
mechanisms to ensure secure access to the framework's resources.
"""

import logging
from flask import Flask, request, jsonify
from threading import Thread
from typing import Optional

from ovadare.agents.agent_registry import AgentRegistry
from ovadare.core.event_dispatcher import EventDispatcher
from ovadare.security.authentication import AuthenticationManager

# Configure the logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class APIEndpoints:
    """
    Defines the API endpoints for the Ovadare Framework.
    """

    def __init__(
        self,
        agent_registry: AgentRegistry,
        event_dispatcher: EventDispatcher,
        authentication_manager: AuthenticationManager
    ) -> None:
        """
        Initializes the APIEndpoints.

        Args:
            agent_registry (AgentRegistry): The registry for managing agents.
            event_dispatcher (EventDispatcher): The event dispatcher for sending events.
            authentication_manager (AuthenticationManager): The authentication manager for securing endpoints.
        """
        self.agent_registry = agent_registry
        self.event_dispatcher = event_dispatcher
        self.authentication_manager = authentication_manager
        self.app = Flask(__name__)
        self._register_routes()
        self._server_thread: Optional[Thread] = None
        logger.debug("APIEndpoints initialized.")

    def _register_routes(self) -> None:
        """
        Registers the API routes.
        """
        @self.app.route('/register', methods=['POST'])
        def register():
            data = request.get_json()
            user_id = data.get('user_id')
            password = data.get('password')
            if not user_id or not password:
                return jsonify({'error': 'user_id and password are required'}), 400
            try:
                self.authentication_manager.register_user(user_id, password)
                return jsonify({'message': 'User registered successfully'}), 201
            except ValueError as e:
                return jsonify({'error': str(e)}), 400

        @self.app.route('/login', methods=['POST'])
        def login():
            data = request.get_json()
            user_id = data.get('user_id')
            password = data.get('password')
            if not user_id or not password:
                return jsonify({'error': 'user_id and password are required'}), 400
            token = self.authentication_manager.authenticate(user_id, password)
            if token:
                return jsonify({'token': token}), 200
            else:
                return jsonify({'error': 'Authentication failed'}), 401

        @self.app.route('/submit_action', methods=['POST'])
        def submit_action():
            token = request.headers.get('Authorization')
            if not self._is_authenticated(token):
                return jsonify({'error': 'Unauthorized'}), 401

            data = request.get_json()
            agent_id = data.get('agent_id')
            action = data.get('action')
            if not agent_id or not action:
                return jsonify({'error': 'agent_id and action are required'}), 400

            # Dispatch the agent action event
            event_data = {'agent_id': agent_id, 'action': action}
            self.event_dispatcher.dispatch('agent_action', event_data)
            logger.info(f"Agent '{agent_id}' submitted action: {action}")
            return jsonify({'message': 'Action submitted successfully'}), 200

        @self.app.route('/submit_feedback', methods=['POST'])
        def submit_feedback():
            token = request.headers.get('Authorization')
            if not self._is_authenticated(token):
                return jsonify({'error': 'Unauthorized'}), 401

            data = request.get_json()
            agent_id = data.get('agent_id')
            feedback_type = data.get('feedback_type')
            message = data.get('message')
            if not agent_id or not feedback_type or not message:
                return jsonify({'error': 'agent_id, feedback_type, and message are required'}), 400

            # Dispatch the feedback event
            feedback_data = {
                'agent_id': agent_id,
                'feedback_type': feedback_type,
                'message': message
            }
            self.event_dispatcher.dispatch('feedback_submitted', feedback_data)
            logger.info(f"Agent '{agent_id}' submitted feedback: {feedback_data}")
            return jsonify({'message': 'Feedback submitted successfully'}), 200

        logger.debug("API routes registered.")

    def _is_authenticated(self, token: Optional[str]) -> bool:
        """
        Checks if the provided token is valid.

        Args:
            token (Optional[str]): The authentication token from the request header.

        Returns:
            bool: True if authenticated, False otherwise.
        """
        if token and self.authentication_manager.validate_token(token):
            return True
        else:
            logger.warning("Unauthorized access attempt.")
            return False

    def start(self, host: str = '0.0.0.0', port: int = 5000) -> None:
        """
        Starts the API server in a separate thread.

        Args:
            host (str): The host IP address.
            port (int): The port number.
        """
        def run_app():
            logger.info(f"API server running on {host}:{port}")
            self.app.run(host=host, port=port, use_reloader=False)

        self._server_thread = Thread(target=run_app, daemon=True)
        self._server_thread.start()
        logger.debug("API server started in a separate thread.")

    def stop(self) -> None:
        """
        Stops the API server.
        """
        # Flask doesn't provide a built-in way to stop the server programmatically.
        # This is a placeholder implementation.
        logger.info("API server stop requested.")
        # Implement server shutdown logic if needed.
        pass
