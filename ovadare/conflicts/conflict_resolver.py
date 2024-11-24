# ovadare/conflicts/conflict_resolver.py

"""
Conflict Resolver Module for the Ovadare Framework

This module provides the ConflictResolver class, which is responsible for resolving
detected conflicts by generating and applying appropriate resolutions based on
predefined strategies.
"""

import logging
from typing import List
from ovadare.conflicts.conflict import Conflict
from ovadare.conflicts.resolution import Resolution
from ovadare.conflicts.resolution_engine import ResolutionEngine
from ovadare.conflicts.conflict_detector import ConflictDetector

# Configure the logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ConflictResolver:
    """
    Resolves detected conflicts by generating and applying resolutions.
    """

    def __init__(self, conflict_detector: ConflictDetector, resolution_engine: ResolutionEngine) -> None:
        """
        Initializes the ConflictResolver.

        Args:
            conflict_detector (ConflictDetector): An instance of ConflictDetector.
            resolution_engine (ResolutionEngine): An instance of ResolutionEngine.
        """
        self.conflict_detector = conflict_detector
        self.resolution_engine = resolution_engine
        logger.debug("ConflictResolver initialized with ConflictDetector and ResolutionEngine.")

    def resolve_conflicts(self, conflicts: List[Conflict]) -> List[Resolution]:
        """
        Resolves a list of conflicts by generating and applying resolutions.

        Args:
            conflicts (List[Conflict]): A list of conflicts to resolve.

        Returns:
            List[Resolution]: A list of generated resolutions.
        """
        logger.debug(f"Resolving {len(conflicts)} conflict(s).")
        resolutions = self.resolution_engine.generate_resolutions(conflicts)
        self.resolution_engine.apply_resolutions(resolutions)
        logger.info(f"Resolved {len(resolutions)} conflict(s).")
        return resolutions
