# tests/test_api_endpoints.py

import unittest
from flask import Flask
from ovadare.communication.api_endpoints import APIEndpoints
from ovadare.agents.agent_registry import AgentRegistry
from ovadare.core.event_dispatcher import EventDispatcher
from ovadare.security.authentication import AuthenticationManager
from ovadare.security.authorization import AuthorizationManager

class TestAPIEndpoints(unittest.TestCase):

    def setUp(self):
        self.agent_registry = AgentRegistry()
        self.event_dispatcher = EventDispatcher()
        self.authentication_manager = AuthenticationManager()
        self.authorization_manager = AuthorizationManager()
        self.api = APIEndpoints(
            agent_registry=self.agent_registry,
            event_dispatcher=self.event_dispatcher,
            authentication_manager=self.authentication_manager,
            authorization_manager=self.authorization_manager
        )
        self.app = self.api.app
        self.client = self.app.test_client()

    def test_register(self):
        # Successful registration
        response = self.client.post('/register', json={'user_id': 'user1', 'password': 'pass1'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered successfully', response.get_data(as_text=True))
        # Duplicate registration
        response = self.client.post('/register', json={'user_id': 'user1', 'password': 'pass1'})
        self.assertEqual(response.status_code, 400)

    def test_login(self):
        # Register a user first
        self.client.post('/register', json={'user_id': 'user2', 'password': 'pass2'})
        # Successful login
        response = self.client.post('/login', json={'user_id': 'user2', 'password': 'pass2'})
        self.assertEqual(response.status_code, 200)
        token = response.get_json().get('token')
        self.assertIsNotNone(token)
        # Failed login
        response = self.client.post('/login', json={'user_id': 'user2', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 401)

    def test_protected_endpoint(self):
        # Register and login to get a token
        self.client.post('/register', json={'user_id': 'user3', 'password': 'pass3'})
        login_response = self.client.post('/login', json={'user_id': 'user3', 'password': 'pass3'})
        token = login_response.get_json().get('token')
        # Access protected endpoint without token
        response = self.client.post('/submit_action', json={'agent_id': 'agent1', 'action': {}})
        self.assertEqual(response.status_code, 401)
        # Access protected endpoint with token but without required permission
        # Revoke 'submit_action' permission
        self.authorization_manager.revoke_role('user3', 'agent')
        self.authorization_manager.assign_role('user3', 'limited_user')
        response = self.client.post('/submit_action', headers={'Authorization': token}, json={'agent_id': 'agent1', 'action': {}})
        self.assertEqual(response.status_code, 403)
        # Assign correct role and try again
        self.authorization_manager.assign_role('user3', 'agent')
        response = self.client.post('/submit_action', headers={'Authorization': token}, json={'agent_id': 'agent1', 'action': {}})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
