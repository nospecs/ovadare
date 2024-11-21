# tests/test_authorization.py

import unittest
from ovadare.security.authorization import AuthorizationManager

class TestAuthorizationManager(unittest.TestCase):

    def setUp(self):
        self.authz_manager = AuthorizationManager()

    def test_assign_and_revoke_role(self):
        # Assign a role to a user
        self.authz_manager.assign_role('user1', 'agent')
        roles = self.authz_manager.get_user_roles('user1')
        self.assertIn('agent', roles)
        # Revoke the role
        self.authz_manager.revoke_role('user1', 'agent')
        roles = self.authz_manager.get_user_roles('user1')
        self.assertNotIn('agent', roles)
        # Attempt to revoke a non-assigned role
        with self.assertRaises(ValueError):
            self.authz_manager.revoke_role('user1', 'admin')

    def test_is_authorized(self):
        # Assign roles and test permissions
        self.authz_manager.assign_role('user2', 'agent')
        is_auth = self.authz_manager.is_authorized('user2', 'submit_action')
        self.assertTrue(is_auth)
        is_auth = self.authz_manager.is_authorized('user2', 'manage_agents')
        self.assertFalse(is_auth)

    def test_add_and_remove_role(self):
        # Add a new role
        self.authz_manager.add_role('supervisor', ['approve_actions', 'view_reports'])
        roles = self.authz_manager._roles_permissions
        self.assertIn('supervisor', roles)
        # Assign the new role to a user
        self.authz_manager.assign_role('user3', 'supervisor')
        is_auth = self.authz_manager.is_authorized('user3', 'approve_actions')
        self.assertTrue(is_auth)
        # Remove the role
        self.authz_manager.remove_role('supervisor')
        roles = self.authz_manager._roles_permissions
        self.assertNotIn('supervisor', roles)
        # Attempt to assign the removed role
        with self.assertRaises(ValueError):
            self.authz_manager.assign_role('user3', 'supervisor')

if __name__ == '__main__':
    unittest.main()
