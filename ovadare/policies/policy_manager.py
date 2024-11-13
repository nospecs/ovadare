# ovadare/policies/policy_manager.py

"""
Policy Manager Module for the Ovadare Framework

This module provides the PolicyManager class, which manages the loading, storage,
and evaluation of policies within the framework. It integrates with the
DynamicPolicyLoader to dynamically load policies from configured sources.
"""

import logging
from typing import List, Optional, Dict, Any
from threading import Lock

from ovadare.policies.policy import Policy, EvaluationResult
from ovadare.policies.dynamic_policy_loader import DynamicPolicyLoader
from ovadare.utils.configuration import Configuration

# Configure the logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PolicyManager:
    """
    The PolicyManager manages the loading, storage, and evaluation of policies.
    It integrates with the DynamicPolicyLoader to load policies from configured sources.
    """

    def __init__(self):
        """
        Initializes the PolicyManager.
        """
        self._policies: List[Policy] = []
        self._lock = Lock()
        self._loader = DynamicPolicyLoader()
        logger.debug("PolicyManager initialized.")

        # Load policies during initialization
        self.load_policies()

    def load_policies(self) -> None:
        """
        Loads policies using the DynamicPolicyLoader from the configured source.
        """
        policy_source = Configuration.get('policy_source', 'policies.json')
        logger.debug(f"Loading policies from source: '{policy_source}'")

        try:
            policies = self._loader.load_policies(source=policy_source)
            with self._lock:
                self._policies = policies
            logger.info(f"{len(policies)} policy(ies) loaded.")
        except Exception as e:
            logger.error(f"Error loading policies from source '{policy_source}': {e}", exc_info=True)

    def get_policies(self) -> List[Policy]:
        """
        Retrieves the list of loaded policies.

        Returns:
            List[Policy]: A list of Policy instances.
        """
        with self._lock:
            policies_copy = self._policies.copy()
        logger.debug(f"Retrieved {len(policies_copy)} policy(ies).")
        return policies_copy

    def get_policy_by_id(self, policy_id: str) -> Optional[Policy]:
        """
        Retrieves a policy by its ID.

        Args:
            policy_id (str): The unique identifier of the policy.

        Returns:
            Optional[Policy]: The Policy instance if found, else None.
        """
        with self._lock:
            for policy in self._policies:
                if policy.policy_id == policy_id:
                    logger.debug(f"Policy '{policy_id}' found.")
                    return policy
        logger.warning(f"Policy '{policy_id}' not found.")
        return None

    def evaluate_policies(self, action: Dict[str, Any]) -> List[EvaluationResult]:
        """
        Evaluates the action against all loaded policies.

        Args:
            action (Dict[str, Any]): The action to evaluate.

        Returns:
            List[EvaluationResult]: A list of evaluation results for each policy.
        """
        results = []
        with self._lock:
            policies_copy = self._policies.copy()

        logger.debug(f"Evaluating action against {len(policies_copy)} policy(ies).")

        for policy in policies_copy:
            try:
                result = policy.evaluate(action)
                results.append(result)
                if not result:
                    logger.info(f"Policy '{policy.policy_id}' violated: {result.message}")
            except Exception as e:
                logger.error(f"Error evaluating policy '{policy.policy_id}': {e}", exc_info=True)
                results.append(EvaluationResult(False, f"Error evaluating policy '{policy.policy_id}': {e}"))

        return results

    def add_policy(self, policy: Policy) -> None:
        """
        Adds a new policy to the manager.

        Args:
            policy (Policy): The policy to add.
        """
        if not isinstance(policy, Policy):
            logger.error("Attempted to add an object that is not a Policy.")
            raise TypeError("policy must be an instance of Policy")

        with self._lock:
            if any(p.policy_id == policy.policy_id for p in self._policies):
                logger.warning(f"Policy '{policy.policy_id}' already exists. Skipping addition.")
                return
            self._policies.append(policy)
            logger.debug(f"Policy '{policy.policy_id}' added.")

    def remove_policy(self, policy_id: str) -> None:
        """
        Removes a policy by its ID.

        Args:
            policy_id (str): The unique identifier of the policy to remove.
        """
        with self._lock:
            original_count = len(self._policies)
            self._policies = [p for p in self._policies if p.policy_id != policy_id]
            if len(self._policies) < original_count:
                logger.debug(f"Policy '{policy_id}' removed.")
            else:
                logger.warning(f"Policy '{policy_id}' not found. Nothing removed.")

    def reload_policies(self) -> None:
        """
        Reloads policies from the configured source.
        """
        logger.info("Reloading policies...")
        self.load_policies()
        logger.info("Policies reloaded.")
