# tests/test_authentication.py

import unittest
from ovadare.security.authentication import AuthenticationManager
import time

class TestAuthenticationManager(unittest.TestCase):

    def setUp(self):
        self.auth_manager = AuthenticationManager()

    def test_register_user(self):
        # Test successful registration
        self.auth_manager.register_user('user1', 'password1')
        self.assertIn('user1', self.auth_manager._users)
        # Test registering an existing user
        with self.assertRaises(ValueError):
            self.auth_manager.register_user('user1', 'password1')

    def test_authenticate(self):
        # Register a user
        self.auth_manager.register_user('user2', 'password2')
        # Test successful authentication
        token = self.auth_manager.authenticate('user2', 'password2')
        self.assertIsNotNone(token)
        # Test authentication with incorrect password
        token = self.auth_manager.authenticate('user2', 'wrongpassword')
        self.assertIsNone(token)
        # Test authentication with non-existent user
        token = self.auth_manager.authenticate('nonexistent', 'password')
        self.assertIsNone(token)

    def test_validate_token(self):
        # Register and authenticate a user
        self.auth_manager.register_user('user3', 'password3')
        token = self.auth_manager.authenticate('user3', 'password3')
        # Test validating a valid token
        is_valid = self.auth_manager.validate_token(token)
        self.assertTrue(is_valid)
        # Test validating an invalid token
        is_valid = self.auth_manager.validate_token('invalidtoken')
        self.assertFalse(is_valid)

    def test_get_user_id_from_token(self):
        # Register and authenticate a user
        self.auth_manager.register_user('user4', 'password4')
        token = self.auth_manager.authenticate('user4', 'password4')
        # Test retrieving user ID from valid token
        user_id = self.auth_manager.get_user_id_from_token(token)
        self.assertEqual(user_id, 'user4')
        # Test retrieving user ID from invalid token
        user_id = self.auth_manager.get_user_id_from_token('invalidtoken')
        self.assertIsNone(user_id)

    def test_token_expiration(self):
        # Register and authenticate a user with short token expiration
        self.auth_manager = AuthenticationManager(token_expiry_duration=1)
        self.auth_manager.register_user('user5', 'password5')
        token = self.auth_manager.authenticate('user5', 'password5')
        # Token should be valid immediately after authentication
        is_valid = self.auth_manager.validate_token(token)
        self.assertTrue(is_valid)
        # Wait for token to expire
        time.sleep(2)
        is_valid = self.auth_manager.validate_token(token)
        self.assertFalse(is_valid)

if __name__ == '__main__':
    unittest.main()
