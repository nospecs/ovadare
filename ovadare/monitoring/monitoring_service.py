# ovadare/monitoring/monitoring_service.py

"""
Monitoring Service Module for the Ovadare Framework

This module provides the MonitoringService class, which collects and reports
metrics and logs for the Ovadare framework. It helps in monitoring system health,
performance, and detecting potential issues.
"""

import logging
import threading
from typing import Optional

from ovadare.agents.agent_registry import AgentRegistry
from ovadare.conflicts.conflict_detector import ConflictDetector

# Configure the logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MonitoringService:
    """
    The MonitoringService collects and reports metrics and logs for the Ovadare framework.
    """

    def __init__(
        self,
        agent_registry: AgentRegistry,
        conflict_detector: ConflictDetector,
        interval: int = 10
    ):
        """
        Initializes the MonitoringService.

        Args:
            agent_registry (AgentRegistry): An instance of AgentRegistry.
            conflict_detector (ConflictDetector): An instance of ConflictDetector.
            interval (int): The interval in seconds at which metrics are collected.
        """
        self.agent_registry = agent_registry
        self.conflict_detector = conflict_detector
        self.interval = interval
        self._stop_event = threading.Event()
        self.thread = threading.Thread(target=self._run, daemon=True)
        logger.debug("MonitoringService initialized with interval %d seconds.", self.interval)

    def start(self):
        """
        Starts the monitoring service in a separate thread.
        """
        logger.info("Starting MonitoringService...")
        self.thread.start()
        logger.info("MonitoringService started.")

    def stop(self):
        """
        Stops the monitoring service.
        """
        logger.info("Stopping MonitoringService...")
        self._stop_event.set()
        self.thread.join()
        logger.info("MonitoringService stopped.")

    def _run(self):
        """
        The main loop that collects and reports metrics at specified intervals.
        """
        while not self._stop_event.is_set():
            try:
                self.collect_metrics()
            except Exception as e:
                logger.error("Error during metric collection: %s", e, exc_info=True)
            self._stop_event.wait(self.interval)

    def collect_metrics(self):
        """
        Collects and logs metrics from various components.
        """
        metrics = {
            'active_agents': self.get_active_agents_count(),
            'conflicts_detected': self.get_conflicts_detected_count(),
        }
        logger.info("Collected Metrics: %s", metrics)

    def get_active_agents_count(self) -> int:
        """
        Retrieves the number of active agents.

        Returns:
            int: The count of active agents.
        """
        active_agents = len(self.agent_registry.get_all_agents())
        logger.debug("Active agents count: %d", active_agents)
        return active_agents

    def get_conflicts_detected_count(self) -> int:
        """
        Retrieves the number of conflicts currently detected.

        Returns:
            int: The count of detected conflicts.
        """
        conflicts_detected = len(self.conflict_detector.get_all_conflicts())
        logger.debug("Conflicts detected count: %d", conflicts_detected)
        return conflicts_detected
