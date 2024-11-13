# ovadare/core/base_classes.py

"""
Base Classes and Interfaces for the Ovadare Framework

This module defines the abstract base classes and interfaces that form the foundation
of the Ovadare conflict detection and resolution framework. These classes establish
the contracts that concrete implementations must adhere to, ensuring consistency
and interoperability across the framework.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime


class AgentInterface(ABC):
    """
    Abstract base class for agents interacting with the Ovadare framework.
    Agents should implement this interface to integrate with the framework.
    """

    @property
    @abstractmethod
    def agent_id(self) -> str:
        """Unique identifier for the agent."""
        pass

    @property
    @abstractmethod
    def capabilities(self) -> List[str]:
        """List of actions or tasks the agent can perform."""
        pass

    @abstractmethod
    def report_action(self, action: Dict[str, Any]) -> None:
        """
        Reports an action that the agent intends to perform to the framework.

        Args:
            action (Dict[str, Any]): The action to be reported.
        """
        pass

    @abstractmethod
    def receive_resolution(self, resolution: 'Resolution') -> None:
        """
        Receives a resolution from the framework.

        Args:
            resolution (Resolution): The resolution to be applied.
        """
        pass


class EvaluationResult:
    """
    Class representing the result of evaluating an action against a policy.
    """

    def __init__(self, compliant: bool, message: Optional[str] = None):
        """
        Initializes an EvaluationResult.

        Args:
            compliant (bool): True if the action complies with the policy, False otherwise.
            message (Optional[str]): Optional message providing details about the evaluation.
        """
        self.compliant = compliant
        self.message = message

    def __bool__(self):
        return self.compliant


class Policy(ABC):
    """
    Abstract base class for policies used in the Ovadare framework.
    Policies define the constraints and requirements that agents must follow.
    """

    @property
    @abstractmethod
    def policy_id(self) -> str:
        """Unique identifier for the policy."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the policy."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Description of the policy."""
        pass

    @property
    @abstractmethod
    def priority(self) -> int:
        """Priority level of the policy (higher value indicates higher priority)."""
        pass

    @abstractmethod
    def evaluate(self, action: Dict[str, Any]) -> 'EvaluationResult':
        """
        Evaluates an action against the policy.

        Args:
            action (Dict[str, Any]): The action to evaluate.

        Returns:
            EvaluationResult: The result of the evaluation.
        """
        pass


class ConflictSeverity(Enum):
    """
    Enumeration for conflict severity levels.
    """
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
    CRITICAL = 'Critical'


class Conflict(ABC):
    """
    Abstract base class for conflicts detected by the Ovadare framework.
    Conflicts represent issues where agent actions clash with policies or constraints.
    """

    @property
    @abstractmethod
    def conflict_id(self) -> str:
        """Unique identifier for the conflict."""
        pass

    @property
    @abstractmethod
    def conflict_type(self) -> str:
        """Type or category of the conflict."""
        pass

    @property
    @abstractmethod
    def related_agent_id(self) -> str:
        """Identifier of the agent involved in the conflict."""
        pass

    @property
    @abstractmethod
    def severity(self) -> ConflictSeverity:
        """Severity level of the conflict."""
        pass

    @property
    @abstractmethod
    def timestamp(self) -> datetime:
        """Timestamp of when the conflict was detected."""
        pass

    @property
    @abstractmethod
    def details(self) -> Dict[str, Any]:
        """
        Additional details about the conflict.

        Returns:
            Dict[str, Any]: A dictionary containing conflict details.
        """
        pass


class Resolution(ABC):
    """
    Abstract base class for resolutions generated by the Ovadare framework.
    Resolutions define the actions to be taken to resolve conflicts.
    """

    @property
    @abstractmethod
    def resolution_id(self) -> str:
        """Unique identifier for the resolution."""
        pass

    @property
    @abstractmethod
    def conflict_id(self) -> str:
        """Identifier of the conflict being resolved."""
        pass

    @property
    @abstractmethod
    def actions(self) -> List[Dict[str, Any]]:
        """List of actions to be taken as part of the resolution."""
        pass

    @property
    @abstractmethod
    def timestamp(self) -> datetime:
        """Timestamp of when the resolution was generated."""
        pass

    @property
    @abstractmethod
    def explanation(self) -> str:
        """
        Provides an explanation for the resolution.

        Returns:
            str: A human-readable explanation of the resolution.
        """
        pass

    @abstractmethod
    def apply(self) -> None:
        """
        Applies the resolution to the affected agent or system.
        """
        pass


class ResolutionStrategy(ABC):
    """
    Abstract base class for resolution strategies.
    Strategies define how conflicts are resolved.
    """

    @abstractmethod
    def resolve(self, conflict: Conflict) -> Resolution:
        """
        Resolves a conflict using a specific strategy.

        Args:
            conflict (Conflict): The conflict to resolve.

        Returns:
            Resolution: The resolution generated for the conflict.
        """
        pass
