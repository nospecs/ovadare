# ovadare/security/authentication.py

import hashlib
import time
import logging

logger = logging.getLogger(__name__)

class AuthenticationManager:
    def __init__(self, token_expiry_duration=3600):
        self._users = {}
        self._tokens = {}
        self.token_expiry_duration = token_expiry_duration

    def register_user(self, user_id, password):
        if user_id in self._users:
            raise ValueError("User already exists.")
        self._users[user_id] = self._hash_password(password)
        logger.info(f"User '{user_id}' registered.")

    def authenticate(self, user_id, password):
        hashed_password = self._users.get(user_id)
        if hashed_password and hashed_password == self._hash_password(password):
            token = self._generate_token(user_id)
            self._tokens[token] = (user_id, time.time())
            logger.info(f"User '{user_id}' authenticated.")
            return token
        logger.warning(f"Authentication failed for user '{user_id}'.")
        return None

    def validate_token(self, token):
        user_data = self._tokens.get(token)
        if user_data:
            user_id, timestamp = user_data
            if time.time() - timestamp < self.token_expiry_duration:
                logger.debug(f"Token for user '{user_id}' is valid.")
                return True
            else:
                logger.debug(f"Token for user '{user_id}' has expired.")
                del self._tokens[token]
        logger.debug("Invalid token.")
        return False

    def get_user_id_from_token(self, token):
        if self.validate_token(token):
            return self._tokens[token][0]
        return None

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def _generate_token(self, user_id):
        token_str = f"{user_id}{time.time()}"
        return hashlib.sha256(token_str.encode()).hexdigest()
