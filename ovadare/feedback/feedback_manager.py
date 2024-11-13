# ovadare/feedback/feedback_manager.py

"""
Feedback Manager Module for the Ovadare Framework

This module provides the FeedbackManager class, which handles the collection,
storage, and processing of feedback from agents and users. The feedback can
be used to improve policies, resolutions, and overall system performance.
"""

import logging
from typing import Dict, Any, List
from threading import Lock

# Configure the logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class FeedbackManager:
    """
    Handles the collection, storage, and processing of feedback from agents and users.
    """

    def __init__(self) -> None:
        """
        Initializes the FeedbackManager.
        """
        self._feedback_store: List[Dict[str, Any]] = []
        self._lock = Lock()
        logger.debug("FeedbackManager initialized.")

    def submit_feedback(self, feedback_data: Dict[str, Any]) -> None:
        """
        Submits feedback to the FeedbackManager.

        Args:
            feedback_data (Dict[str, Any]): A dictionary containing feedback details.
                Expected keys include 'agent_id', 'user_id', 'feedback_type',
                'message', and 'timestamp'.
        """
        required_keys = {'feedback_type', 'message', 'timestamp'}
        if not required_keys.issubset(feedback_data.keys()):
            logger.error("Feedback data is missing required keys.")
            raise ValueError(f"Feedback data must include {required_keys}")

        logger.debug(f"Submitting feedback: {feedback_data}")
        with self._lock:
            self._feedback_store.append(feedback_data)
        logger.info("Feedback submitted successfully.")

    def get_all_feedback(self) -> List[Dict[str, Any]]:
        """
        Retrieves all submitted feedback.

        Returns:
            List[Dict[str, Any]]: A list of all feedback entries.
        """
        with self._lock:
            feedback_copy = self._feedback_store.copy()
        logger.debug(f"Retrieved {len(feedback_copy)} feedback entries.")
        return feedback_copy

    def get_feedback_by_agent(self, agent_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves feedback submitted by a specific agent.

        Args:
            agent_id (str): The ID of the agent.

        Returns:
            List[Dict[str, Any]]: A list of feedback entries from the specified agent.
        """
        with self._lock:
            agent_feedback = [fb for fb in self._feedback_store if fb.get('agent_id') == agent_id]
        logger.debug(f"Retrieved {len(agent_feedback)} feedback entries for agent '{agent_id}'.")
        return agent_feedback

    def process_feedback(self) -> None:
        """
        Processes collected feedback to identify trends or issues.
        This method can be expanded to include analytics or integration
        with policy updates.
        """
        logger.debug("Processing feedback...")
        with self._lock:
            total_feedback = len(self._feedback_store)
            # Placeholder for processing logic
            if total_feedback == 0:
                logger.info("No feedback to process.")
                return

            # Example processing: simple count of feedback types
            feedback_types = {}
            for fb in self._feedback_store:
                f_type = fb.get('feedback_type', 'unknown')
                feedback_types[f_type] = feedback_types.get(f_type, 0) + 1

            logger.info(f"Processed {total_feedback} feedback entries.")
            logger.debug(f"Feedback types count: {feedback_types}")

            # After processing, feedback could be archived or retained
            # For simplicity, we're not clearing the feedback store here
