# tests/autogen_tests.py

from autogen.agent import Agent
from autogen.environment import Environment
import requests
import unittest
import time

# Import any other necessary modules

class TestAgent(Agent):
    def __init__(self, agent_id, api_base_url):
        super().__init__(agent_id)
        self.api_base_url = api_base_url
        self.token = None  # To store authentication token

    def run(self):
        # Simulate agent registration and login
        self.register()
        self.login()
        # Perform actions
        self.submit_action()
        # Submit feedback
        self.submit_feedback()

    def register(self):
        url = f"{self.api_base_url}/register"
        data = {'user_id': self.agent_id, 'password': 'password123'}
        response = requests.post(url, json=data)
        if response.status_code == 201:
            print(f"{self.agent_id}: Registration successful.")
        else:
            print(f"{self.agent_id}: Registration failed. Response: {response.text}")

    def login(self):
        url = f"{self.api_base_url}/login"
        data = {'user_id': self.agent_id, 'password': 'password123'}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            self.token = response.json().get('token')
            print(f"{self.agent_id}: Login successful. Token obtained.")
        else:
            print(f"{self.agent_id}: Login failed. Response: {response.text}")

    def submit_action(self):
        url = f"{self.api_base_url}/submit_action"
        headers = {'Authorization': self.token}
        action_data = {'type': 'test_action', 'timestamp': time.time()}
        data = {'agent_id': self.agent_id, 'action': action_data}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print(f"{self.agent_id}: Action submitted successfully.")
        else:
            print(f"{self.agent_id}: Action submission failed. Response: {response.text}")

    def submit_feedback(self):
        url = f"{self.api_base_url}/submit_feedback"
        headers = {'Authorization': self.token}
        feedback_data = {
            'agent_id': self.agent_id,
            'feedback_type': 'test_feedback',
            'message': 'This is a test feedback.'
        }
        response = requests.post(url, headers=headers, json=feedback_data)
        if response.status_code == 200:
            print(f"{self.agent_id}: Feedback submitted successfully.")
        else:
            print(f"{self.agent_id}: Feedback submission failed. Response: {response.text}")


def fetch_conflicts(api_base_url):
    url = f"{api_base_url}/get_conflicts"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('conflicts', [])
    else:
        print(f"Failed to fetch conflicts. Response: {response.text}")
        return []

def fetch_resolutions(api_base_url):
    url = f"{api_base_url}/get_resolutions"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('resolutions', [])
    else:
        print(f"Failed to fetch resolutions. Response: {response.text}")
        return []

class AutoGenTestCases(unittest.TestCase):

    def test_conflict_scenario(self):
        api_base_url = 'http://localhost:5000'

        # Instantiate agents
        agent1 = TestAgent('agent1', api_base_url)
        agent2 = TestAgent('agent2', api_base_url)

        # Run agents in the environment
        env = Environment(agents=[agent1, agent2])
        env.run()

        # Give some time for the framework to process
        time.sleep(2)

        # Fetch conflicts and resolutions
        conflicts = fetch_conflicts(api_base_url)
        resolutions = fetch_resolutions(api_base_url)

        # Assert that conflicts were detected
        self.assertTrue(len(conflicts) > 0, "No conflicts were detected when expected.")

        # Assert that resolutions were applied
        self.assertEqual(len(conflicts), len(resolutions), "Resolutions were not applied to all conflicts.")

if __name__ == '__main__':
    unittest.main()
