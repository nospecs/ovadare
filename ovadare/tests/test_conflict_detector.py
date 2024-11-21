# tests/test_conflict_detector.py

import unittest
import os
import json
from ovadare.conflicts.conflict_detector import ConflictDetector
from ovadare.policies.policy_manager import PolicyManager
from ovadare.conflicts.conflict import Conflict

class TestConflictDetector(unittest.TestCase):

    def setUp(self):
        # Set up a PolicyManager with a simple policy
        self.policy_manager = PolicyManager()
        self.policy_manager.policies = [
            {'id': 'policy1', 'condition': lambda action: action.get('type') != 'forbidden', 'description': 'Action must not be forbidden'}
        ]
        # Set up a ConflictDetector
        self.conflict_detector = ConflictDetector(policy_manager=self.policy_manager)
        # Ensure a clean state
        self.conflict_detector.conflicts = []
        self.conflict_detector.conflict_storage_file = 'test_conflicts_data.json'
        # Remove the test conflicts file if it exists
        if os.path.exists(self.conflict_detector.conflict_storage_file):
            os.remove(self.conflict_detector.conflict_storage_file)

    def tearDown(self):
        # Clean up the test conflicts file
        if os.path.exists(self.conflict_detector.conflict_storage_file):
            os.remove(self.conflict_detector.conflict_storage_file)

    def test_detect_conflict(self):
        # Action that violates the policy
        action = {'type': 'forbidden'}
        conflicts = self.conflict_detector.detect('agent1', action)
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0].agent_id, 'agent1')
        # Action that complies with the policy
        action = {'type': 'allowed'}
        conflicts = self.conflict_detector.detect('agent1', action)
        self.assertEqual(len(conflicts), 0)

    def test_persistent_storage(self):
        # Detect a conflict to trigger saving
        action = {'type': 'forbidden'}
        self.conflict_detector.detect('agent2', action)
        # Load conflicts from storage
        self.conflict_detector.load_conflicts()
        self.assertEqual(len(self.conflict_detector.conflicts), 1)
        self.assertEqual(self.conflict_detector.conflicts[0].agent_id, 'agent2')

if __name__ == '__main__':
    unittest.main()
