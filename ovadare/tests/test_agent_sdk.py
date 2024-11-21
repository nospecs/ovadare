# tests/test_agent_sdk.py

import unittest
from unittest.mock import patch
from ovadare.agents.agent_sdk import AgentSDK

class TestAgentSDK(unittest.TestCase):

    @patch('ovadare.agents.agent_sdk.requests.post')
    def test_register(self, mock_post):
        # Mock the response for registration
        mock_post.return_value.status_code = 201
        sdk = AgentSDK(api_base_url='http://localhost:5000', authentication_manager=None, authorization_manager=None)
        result = sdk.register('agent1', 'password1')
        self.assertTrue(result)

    @patch('ovadare.agents.agent_sdk.requests.post')
    def test_login(self, mock_post):
        # Mock the response for login
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'token': 'validtoken'}
        sdk = AgentSDK(api_base_url='http://localhost:5000', authentication_manager=None, authorization_manager=None)
        result = sdk.login('agent1', 'password1')
        self.assertTrue(result)
        self.assertEqual(sdk.token, 'validtoken')

    @patch('ovadare.agents.agent_sdk.requests.post')
    def test_submit_action(self, mock_post):
        # Mock the response for action submission
        mock_post.return_value.status_code = 200
        sdk = AgentSDK(api_base_url='http://localhost:5000', authentication_manager=None, authorization_manager=None)
        sdk.agent_id = 'agent1'
        sdk.token = 'validtoken'
        result = sdk.submit_action({'action_type': 'test_action'})
        self.assertTrue(result)

    @patch('ovadare.agents.agent_sdk.requests.post')
    def test_submit_feedback(self, mock_post):
        # Mock the response for feedback submission
        mock_post.return_value.status_code = 200
        sdk = AgentSDK(api_base_url='http://localhost:5000', authentication_manager=None, authorization_manager=None)
        sdk.agent_id = 'agent1'
        sdk.token = 'validtoken'
        result = sdk.submit_feedback('test_feedback', 'This is a test.')
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
