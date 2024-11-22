# ovadare/conflicts/resolution_engine.py

"""
Resolution Engine Module for the Ovadare Framework

This module provides the ResolutionEngine class, which is responsible for
generating resolutions for detected conflicts and communicating them to
the appropriate agents.
"""

import logging
from typing import List, Optional
from threading import Lock

from ovadare.conflicts.conflict import Conflict
from ovadare.conflicts.resolution import Resolution
from ovadare.agents.agent_interface import AgentInterface
from ovadare.agents.agent_registry import AgentRegistry

# Configure the logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ResolutionEngine:
    """
    The ResolutionEngine generates resolutions for detected conflicts and
    communicates them to the appropriate agents.
    """

    def __init__(self, agent_registry: Optional[AgentRegistry] = None):
        """
        Initializes the ResolutionEngine.

        Args:
            agent_registry (Optional[AgentRegistry]): An instance of AgentRegistry.
                If None, a new AgentRegistry is created.
        """
        self.agent_registry = agent_registry or AgentRegistry()
        self._lock = Lock()
        logger.debug("ResolutionEngine initialized.")

    def generate_resolutions(self, conflicts: List[Conflict]) -> List[Resolution]:
        """
        Generates resolutions for a list of conflicts.

        Args:
            conflicts (List[Conflict]): A list of conflicts to resolve.

        Returns:
            List[Resolution]: A list of generated resolutions.
        """
        resolutions = []
        logger.debug(f"Generating resolutions for {len(conflicts)} conflict(s).")

        with self._lock:
            for conflict in conflicts:
                try:
                    resolution = self._create_resolution(conflict)
                    resolutions.append(resolution)
                    logger.info(
                        f"Resolution '{resolution.resolution_id}' generated for conflict '{conflict.conflict_id}'."
                    )
                except Exception as e:
                    logger.error(
                        f"Error generating resolution for conflict '{conflict.conflict_id}': {e}",
                        exc_info=True
                    )

        return resolutions

    def _create_resolution(self, conflict: Conflict) -> Resolution:
        """
        Creates a resolution for a single conflict.

        Args:
            conflict (Conflict): The conflict to resolve.

        Returns:
            Resolution: The generated resolution.
        """
        explanation = f"Resolution for conflict '{conflict.conflict_id}': {conflict.violation_details}"

        # Placeholder for corrective action
        corrective_action = {
            'action': 'notify',
            'details': {
                'message': f"Please adjust your action to comply with policy '{conflict.policy_id}'."
            }
        }

        resolution = Resolution(
            conflict_id=conflict.conflict_id,
            corrective_action=corrective_action,
            explanation=explanation
        )

        logger.debug(f"Resolution created: {resolution}")
        return resolution

    def apply_resolutions(self, resolutions: List[Resolution]) -> None:
        """
        Applies a list of resolutions by communicating them to the appropriate agents.

        Args:
            resolutions (List[Resolution]): The resolutions to apply.
        """
        logger.debug(f"Applying {len(resolutions)} resolution(s).")

        with self._lock:
            for resolution in resolutions:
                try:
                    conflict = self._get_conflict_by_id(resolution.conflict_id)
                    if not conflict:
                        logger.warning(f"Conflict '{resolution.conflict_id}' not found. Cannot apply resolution.")
                        continue

                    agent = self.agent_registry.get_agent(conflict.related_agent_id)
                    if not agent:
                        logger.warning(
                            f"Agent '{conflict.related_agent_id}' not found. Cannot apply resolution '{resolution.resolution_id}'."
                        )
                        continue

                    self._send_resolution_to_agent(agent, resolution)
                    logger.info(
                        f"Resolution '{resolution.resolution_id}' applied to agent '{agent.agent_id}'."
                    )
                except Exception as e:
                    logger.error(
                        f"Error applying resolution '{resolution.resolution_id}': {e}",
                        exc_info=True
                    )

    def _get_conflict_by_id(self, conflict_id: str) -> Optional[Conflict]:
        """
        Retrieves a conflict by its ID.

        Args:
            conflict_id (str): The unique identifier of the conflict.

        Returns:
            Optional[Conflict]: The Conflict instance if found, else None.
        """
        # This method assumes that the ResolutionEngine has access to the conflicts.
        # In practice, this may involve querying a ConflictStore or similar component.
        # For this example, we'll assume conflicts are stored in a dictionary.
        logger.debug(f"Retrieving conflict '{conflict_id}'.")
        # Placeholder implementation
        return None  # Needs implementation based on actual conflict storage

    def _send_resolution_to_agent(self, agent: AgentInterface, resolution: Resolution) -> None:
        """
        Sends a resolution to an agent.

        Args:
            agent (AgentInterface): The agent to send the resolution to.
            resolution (Resolution): The resolution to send.
        """
        try:
            agent.handle_resolution(resolution)
            logger.debug(
                f"Resolution '{resolution.resolution_id}' sent to agent '{agent.agent_id}'."
            )
        except Exception as e:
            logger.error(
                f"Error sending resolution to agent '{agent.agent_id}': {e}",
                exc_info=True
            )


def load_resolutions(self):
    """
    Loads resolutions from persistent storage.
    """
    if os.path.exists(self.resolution_storage_file):
        with open(self.resolution_storage_file, 'r', encoding='utf-8') as f:
            resolutions_data = json.load(f)
            self.resolutions = [Resolution.deserialize(data) for data in resolutions_data]
    return self.resolutions
