# ovadare/policies/dynamic_policy_loader.py

"""
Dynamic Policy Loader Module for the Ovadare Framework

This module provides the DynamicPolicyLoader class, which is responsible for
loading policies from various sources, such as JSON files, databases, or APIs.
"""

from typing import List, Optional, Callable
import logging
import json
import os

from ovadare.policies.policy import Policy, ConcretePolicy, PolicyRule, PolicyPriority

# Configure the logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class DynamicPolicyLoader:
    """
    The DynamicPolicyLoader is responsible for loading policies from a specified source.
    """

    def __init__(self):
        """
        Initializes the DynamicPolicyLoader.
        """
        logger.debug("DynamicPolicyLoader initialized.")

    def load_policies(self, source: Optional[str] = None) -> List[Policy]:
        """
        Loads policies from the specified source.

        Args:
            source (Optional[str]): The source from which to load policies.
                If None, a default source is used (e.g., 'policies.json').

        Returns:
            List[Policy]: A list of loaded Policy instances.
        """
        source = source or 'policies.json'
        logger.debug(f"Loading policies from source: '{source}'")

        if not os.path.exists(source):
            logger.error(f"Policy source '{source}' not found.")
            return []

        try:
            with open(source, 'r') as f:
                policies_data = json.load(f)
        except Exception as e:
            logger.error(f"Error reading policy source '{source}': {e}", exc_info=True)
            return []

        policies = []
        for policy_dict in policies_data.get('policies', []):
            try:
                policy = self._parse_policy(policy_dict)
                policies.append(policy)
                logger.debug(f"Policy '{policy.policy_id}' loaded.")
            except Exception as e:
                logger.error(f"Error parsing policy: {e}", exc_info=True)

        logger.info(f"Total policies loaded: {len(policies)}")
        return policies

    def _parse_policy(self, policy_dict: dict) -> Policy:
        """
        Parses a dictionary representing a policy into a Policy instance.

        Args:
            policy_dict (dict): The dictionary containing policy data.

        Returns:
            Policy: An instance of a Policy.

        Raises:
            ValueError: If required fields are missing or invalid.
        """
        policy_id = policy_dict.get('policy_id')
        name = policy_dict.get('name')
        description = policy_dict.get('description', '')
        priority_str = policy_dict.get('priority', 'MEDIUM')
        rules_data = policy_dict.get('rules', [])

        if not policy_id or not name or not rules_data:
            raise ValueError("Policy must have 'policy_id', 'name', and at least one 'rule'.")

        try:
            priority = PolicyPriority[priority_str.upper()]
        except KeyError:
            raise ValueError(f"Invalid policy priority: '{priority_str}'.")

        policy = ConcretePolicy(
            policy_id=policy_id,
            name=name,
            description=description,
            priority=priority
        )

        for rule_dict in rules_data:
            rule = self._parse_rule(rule_dict)
            policy.add_rule(rule)

        return policy

    def _parse_rule(self, rule_dict: dict) -> PolicyRule:
        """
        Parses a dictionary representing a policy rule into a PolicyRule instance.

        Args:
            rule_dict (dict): The dictionary containing rule data.

        Returns:
            PolicyRule: An instance of a PolicyRule.

        Raises:
            ValueError: If required fields are missing or invalid.
        """
        rule_id = rule_dict.get('rule_id')
        condition_code = rule_dict.get('condition')
        message = rule_dict.get('message')

        if not rule_id or not condition_code or not message:
            raise ValueError("Rule must have 'rule_id', 'condition', and 'message'.")

        # Compile the condition code into a callable function
        condition = self._compile_condition(condition_code, rule_id)

        rule = PolicyRule(
            rule_id=rule_id,
            condition=condition,
            message=message
        )

        return rule

    def _compile_condition(self, condition_code: str, rule_id: str) -> Callable:
        """
        Compiles a condition code string into a callable function.

        Args:
            condition_code (str): The code representing the condition.
            rule_id (str): The ID of the rule, used for logging.

        Returns:
            Callable: A function that evaluates the condition.

        Raises:
            Exception: If the condition code cannot be compiled.
        """
        try:
            # Define a safe namespace for execution
            exec_globals = {'__builtins__': {}}
            exec_locals = {}

            # Define allowed built-in functions (if any)
            allowed_builtins = {
                'len': len,
                'max': max,
                'min': min,
                # Add other safe built-ins if needed
            }
            exec_globals['__builtins__'] = allowed_builtins

            # Compile the condition code
            compiled_code = compile(condition_code, '<string>', 'exec')
            exec(compiled_code, exec_globals, exec_locals)
            condition_func = exec_locals.get('condition')
            if not condition_func:
                raise ValueError("Condition code must define a 'condition' function.")
            if not callable(condition_func):
                raise ValueError("'condition' must be a callable function.")
            logger.debug(f"Condition function compiled for rule '{rule_id}'.")
            return condition_func
        except Exception as e:
            logger.error(f"Error compiling condition code for rule '{rule_id}': {e}", exc_info=True)
            raise
