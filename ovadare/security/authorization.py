# ovadare/security/authorization.py

"""
Authorization Module for the Ovadare Framework

This module provides the AuthorizationManager class, which handles role-based
access control (RBAC) to manage permissions for users and agents. It defines
roles, permissions, and provides methods to check if a user or agent is authorized
to perform a specific action.
"""

import logging
from typing import Dict, List, Set

# Configure the logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class AuthorizationManager:
    """
    Manages authorization by assigning roles and permissions to users and agents.
    Provides methods to check if an entity is authorized to perform a specific action.
    """

    def __init__(self) -> None:
        """
        Initializes the AuthorizationManager with default roles and permissions.
        """
        self._roles_permissions: Dict[str, Set[str]] = {}
        self._user_roles: Dict[str, Set[str]] = {}
        self._initialize_default_roles()
        logger.debug("AuthorizationManager initialized.")

    def _initialize_default_roles(self) -> None:
        """
        Initializes default roles and their associated permissions.
        """
        # Define default roles and permissions
        self._roles_permissions = {
            'agent': {'submit_action', 'submit_feedback'},
            'admin': {'submit_action', 'submit_feedback', 'manage_agents', 'manage_policies'}
        }
        logger.debug("Default roles and permissions initialized.")

    def assign_role(self, user_id: str, role: str) -> None:
        """
        Assigns a role to a user or agent.

        Args:
            user_id (str): The ID of the user or agent.
            role (str): The role to assign.

        Raises:
            ValueError: If the role is not defined.
        """
        if role not in self._roles_permissions:
            logger.error(f"Role '{role}' is not defined.")
            raise ValueError(f"Role '{role}' is not defined.")

        roles = self._user_roles.setdefault(user_id, set())
        roles.add(role)
        logger.info(f"Role '{role}' assigned to user '{user_id}'.")

    def revoke_role(self, user_id: str, role: str) -> None:
        """
        Revokes a role from a user or agent.

        Args:
            user_id (str): The ID of the user or agent.
            role (str): The role to revoke.

        Raises:
            ValueError: If the role is not assigned to the user.
        """
        roles = self._user_roles.get(user_id)
        if not roles or role not in roles:
            logger.error(f"User '{user_id}' does not have role '{role}'.")
            raise ValueError(f"User '{user_id}' does not have role '{role}'.")
        roles.remove(role)
        logger.info(f"Role '{role}' revoked from user '{user_id}'.")

    def is_authorized(self, user_id: str, permission: str) -> bool:
        """
        Checks if the user or agent has the specified permission.

        Args:
            user_id (str): The ID of the user or agent.
            permission (str): The permission to check.

        Returns:
            bool: True if authorized, False otherwise.
        """
        roles = self._user_roles.get(user_id, set())
        for role in roles:
            permissions = self._roles_permissions.get(role, set())
            if permission in permissions:
                logger.debug(f"User '{user_id}' is authorized for permission '{permission}'.")
                return True
        logger.warning(f"User '{user_id}' is not authorized for permission '{permission}'.")
        return False

    def add_role(self, role: str, permissions: List[str]) -> None:
        """
        Adds a new role with the specified permissions.

        Args:
            role (str): The name of the new role.
            permissions (List[str]): A list of permissions for the role.
        """
        if role in self._roles_permissions:
            logger.error(f"Role '{role}' already exists.")
            raise ValueError(f"Role '{role}' already exists.")
        self._roles_permissions[role] = set(permissions)
        logger.info(f"Role '{role}' added with permissions: {permissions}")

    def remove_role(self, role: str) -> None:
        """
        Removes an existing role.

        Args:
            role (str): The name of the role to remove.

        Raises:
            ValueError: If the role does not exist.
        """
        if role not in self._roles_permissions:
            logger.error(f"Role '{role}' does not exist.")
            raise ValueError(f"Role '{role}' does not exist.")
        del self._roles_permissions[role]
        logger.info(f"Role '{role}' removed.")

    def get_user_roles(self, user_id: str) -> List[str]:
        """
        Retrieves the list of roles assigned to a user.

        Args:
            user_id (str): The ID of the user or agent.

        Returns:
            List[str]: A list of role names.
        """
        roles = list(self._user_roles.get(user_id, set()))
        logger.debug(f"User '{user_id}' has roles: {roles}")
        return roles

    def get_role_permissions(self, role: str) -> List[str]:
        """
        Retrieves the list of permissions associated with a role.

        Args:
            role (str): The name of the role.

        Returns:
            List[str]: A list of permissions.

        Raises:
            ValueError: If the role does not exist.
        """
        if role not in self._roles_permissions:
            logger.error(f"Role '{role}' does not exist.")
            raise ValueError(f"Role '{role}' does not exist.")
        permissions = list(self._roles_permissions[role])
        logger.debug(f"Role '{role}' has permissions: {permissions}")
        return permissions
