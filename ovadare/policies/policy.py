# ovadare/policies/policy.py

"""
Policy Module for the Ovadare Framework

This module provides the abstract Policy class and concrete implementations for defining
and evaluating policies within the framework. It includes the PolicyRule class for
defining individual rules that make up a policy.
"""

from abc import ABC, abstractmethod
from typing import List, Callable
import logging

# Configure the logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class EvaluationResult:
    """
    Represents the result of evaluating a policy or rule.
    """

    def __init__(self, success: bool, message: str = ""):
        self.success = success
        self.message = message

    def __bool__(self):
        return self.success

    def __repr__(self):
        return f"EvaluationResult(success={self.success}, message='{self.message}')"


class PolicyPriority:
    """
    Enum-like class for policy priorities.
    """
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'


class PolicyRule:
    """
    Represents a single rule within a policy.
    """

    def __init__(self, rule_id: str, condition: Callable[[dict], bool], message: str):
        """
        Initializes a PolicyRule.

        Args:
            rule_id (str): The unique identifier of the rule.
            condition (Callable[[dict], bool]): A function that evaluates the rule condition.
            message (str): The message to return if the rule is violated.
        """
        self.rule_id = rule_id
        self.condition = condition
        self.message = message

    def evaluate(self, action: dict) -> EvaluationResult:
        """
        Evaluates the rule against an action.

        Args:
            action (dict): The action to evaluate.

        Returns:
            EvaluationResult: The result of the evaluation.
        """
        try:
            if self.condition(action):
                logger.debug(f"Rule '{self.rule_id}' passed.")
                return EvaluationResult(True)
            else:
                logger.info(f"Rule '{self.rule_id}' violated: {self.message}")
                return EvaluationResult(False, self.message)
        except Exception as e:
            logger.error(f"Error evaluating rule '{self.rule_id}': {e}", exc_info=True)
            return EvaluationResult(False, f"Error evaluating rule '{self.rule_id}': {e}")


class Policy(ABC):
    """
    Abstract base class for policies.
    """

    @property
    @abstractmethod
    def policy_id(self) -> str:
        pass

    @abstractmethod
    def evaluate(self, action: dict) -> EvaluationResult:
        pass


class ConcretePolicy(Policy):
    """
    A concrete implementation of a policy consisting of multiple rules.
    """

    def __init__(self, policy_id: str, name: str, description: str, priority: str = PolicyPriority.MEDIUM):
        """
        Initializes a ConcretePolicy.

        Args:
            policy_id (str): The unique identifier of the policy.
            name (str): The name of the policy.
            description (str): A description of the policy.
            priority (str): The priority level of the policy.
        """
        self._policy_id = policy_id
        self.name = name
        self.description = description
        self.priority = priority
        self.rules: List[PolicyRule] = []
        logger.debug(f"Policy '{self.policy_id}' initialized with priority '{self.priority}'.")

    @property
    def policy_id(self) -> str:
        return self._policy_id

    def add_rule(self, rule: PolicyRule) -> None:
        """
        Adds a rule to the policy.

        Args:
            rule (PolicyRule): The rule to add.
        """
        if not isinstance(rule, PolicyRule):
            logger.error("Attempted to add an object that is not a PolicyRule.")
            raise TypeError("rule must be an instance of PolicyRule")
        self.rules.append(rule)
        logger.debug(f"Rule '{rule.rule_id}' added to policy '{self.policy_id}'.")

    def evaluate(self, action: dict) -> EvaluationResult:
        """
        Evaluates the action against all rules in the policy.

        Args:
            action (dict): The action to evaluate.

        Returns:
            EvaluationResult: The overall result of the policy evaluation.
        """
        logger.debug(f"Evaluating action against policy '{self.policy_id}'.")
        for rule in self.rules:
            result = rule.evaluate(action)
            if not result:
                logger.info(f"Policy '{self.policy_id}' violated: {result.message}")
                return EvaluationResult(False, result.message)
        logger.debug(f"Action complies with policy '{self.policy_id}'.")
        return EvaluationResult(True)
