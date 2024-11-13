# ovadare/conflicts/conflict_detector.py

"""
Conflict Detector Module for the Ovadare Framework

This module provides the ConflictDetector class, which is responsible for detecting
policy violations by evaluating agent actions against the loaded policies.
It stores detected conflicts and provides methods for retrieving and resolving them.
"""

import logging
import json
import os
from typing import List, Dict, Any, Optional
from threading import Lock

from ovadare.policies.policy_manager import PolicyManager
from ovadare.conflicts.conflict import Conflict
from ovadare.utils.configuration import Configuration

# Configure the logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ConflictDetector:
    """
    Evaluates agent actions against policies to detect conflicts.
    """

    def __init__(self, policy_manager: Optional[PolicyManager] = None) -> None:
        """
        Initializes the ConflictDetector.

        Args:
            policy_manager (Optional[PolicyManager]): An instance of PolicyManager.
                If None, a new PolicyManager is created.
        """
        self.policy_manager = policy_manager or PolicyManager()
        self._conflicts: Dict[str, Conflict] = {}
        self._lock = Lock()
        self._storage_file = Configuration.get('conflict_storage_file', 'conflicts_data.json')
        self._load_conflicts()
        logger.debug("ConflictDetector initialized.")

    def detect(self, agent_id: str, action: Dict[str, Any]) -> List[Conflict]:
        """
        Detects conflicts by evaluating an agent's action against policies.

        Args:
            agent_id (str): The ID of the agent performing the action.
            action (Dict[str, Any]): The action to evaluate.

        Returns:
            List[Conflict]: A list of detected conflicts.
        """
        conflicts = []
        logger.debug(f"Detecting conflicts for agent '{agent_id}' and action: {action}")

        try:
            evaluation_results = self.policy_manager.evaluate_policies(action)
            for result in evaluation_results:
                if not result.is_compliant:
                    conflict = Conflict(
                        related_agent_id=agent_id,
                        action=action,
                        violation_details=result.message,
                        policy_id=result.policy_id
                    )
                    with self._lock:
                        self._conflicts[conflict.conflict_id] = conflict
                        self._save_conflicts()
                    conflicts.append(conflict)
                    logger.info(f"Conflict detected: {conflict}")
        except Exception as e:
            logger.error(f"Error during conflict detection for agent '{agent_id}': {e}", exc_info=True)

        return conflicts

    def get_conflict_by_id(self, conflict_id: str) -> Optional[Conflict]:
        """
        Retrieves a conflict by its ID.

        Args:
            conflict_id (str): The unique identifier of the conflict.

        Returns:
            Optional[Conflict]: The Conflict instance if found, else None.
        """
        with self._lock:
            conflict = self._conflicts.get(conflict_id)
        if conflict:
            logger.debug(f"Conflict '{conflict_id}' retrieved.")
        else:
            logger.warning(f"Conflict '{conflict_id}' not found.")
        return conflict

    def get_all_conflicts(self) -> List[Conflict]:
        """
        Retrieves all detected conflicts.

        Returns:
            List[Conflict]: A list of all detected conflicts.
        """
        with self._lock:
            conflicts = list(self._conflicts.values())
        logger.debug(f"Retrieved {len(conflicts)} conflict(s).")
        return conflicts

    def resolve_conflict(self, conflict_id: str) -> None:
        """
        Resolves a conflict by removing it from the stored conflicts.

        Args:
            conflict_id (str): The unique identifier of the conflict to resolve.
        """
        with self._lock:
            if conflict_id in self._conflicts:
                del self._conflicts[conflict_id]
                self._save_conflicts()
                logger.info(f"Conflict '{conflict_id}' resolved and removed.")
            else:
                logger.warning(f"Conflict '{conflict_id}' not found. Cannot resolve.")

    def clear_conflicts(self) -> None:
        """
        Clears all stored conflicts.
        """
        with self._lock:
            self._conflicts.clear()
            self._save_conflicts()
        logger.info("All conflicts cleared.")

    def _load_conflicts(self) -> None:
        """
        Loads conflicts data from the storage file.
        """
        if os.path.exists(self._storage_file):
            try:
                with open(self._storage_file, 'r', encoding='utf-8') as f:
                    conflicts_data = json.load(f)
                    self._conflicts = {
                        cid: Conflict.from_dict(cdata) for cid, cdata in conflicts_data.items()
                    }
                logger.debug(f"Loaded conflicts data from '{self._storage_file}'.")
            except Exception as e:
                logger.error(f"Failed to load conflicts data: {e}", exc_info=True)
                self._conflicts = {}
        else:
            logger.debug(f"Conflict storage file '{self._storage_file}' does not exist. Starting fresh.")

    def _save_conflicts(self) -> None:
        """
        Saves conflicts data to the storage file.
        """
        try:
            conflicts_data = {cid: conflict.to_dict() for cid, conflict in self._conflicts.items()}
            with open(self._storage_file, 'w', encoding='utf-8') as f:
                json.dump(conflicts_data, f, ensure_ascii=False, indent=4)
            logger.debug(f"Saved conflicts data to '{self._storage_file}'.")
        except Exception as e:
            logger.error(f"Failed to save conflicts data: {e}", exc_info=True)
