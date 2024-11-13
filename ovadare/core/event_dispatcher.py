# ovadare/core/event_dispatcher.py

"""
Event Dispatcher Module for the Ovadare Framework

This module provides the EventDispatcher class, which facilitates the registration,
deregistration, and notification of event listeners within the framework.
"""

from typing import Callable, Dict, List, Any
from threading import Lock
import logging

# Configure the logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class EventDispatcher:
    """
    The EventDispatcher is responsible for managing event listeners and dispatching
    events to the appropriate listeners in a thread-safe manner.
    """

    def __init__(self):
        """
        Initializes the EventDispatcher with an empty listener registry and a lock
        for thread-safe operations.
        """
        self._listeners: Dict[str, List[Callable[..., None]]] = {}
        self._lock = Lock()
        logger.debug("EventDispatcher initialized with an empty listener registry.")

    def register_listener(self, event_type: str, listener: Callable[..., None]) -> None:
        """
        Registers a listener for a specific event type.

        Args:
            event_type (str): The type of event to listen for.
            listener (Callable[..., None]): The callback function to invoke when the event occurs.
        """
        if not callable(listener):
            logger.error("Listener must be callable.")
            raise TypeError("Listener must be callable.")

        with self._lock:
            listeners = self._listeners.setdefault(event_type, [])
            if listener not in listeners:
                listeners.append(listener)
                logger.debug(f"Listener '{listener.__name__}' registered for event type '{event_type}'.")
            else:
                logger.warning(f"Listener '{listener.__name__}' is already registered for event type '{event_type}'.")

    def deregister_listener(self, event_type: str, listener: Callable[..., None]) -> None:
        """
        Deregisters a listener from a specific event type.

        Args:
            event_type (str): The type of event the listener was registered for.
            listener (Callable[..., None]): The listener to remove.
        """
        with self._lock:
            listeners = self._listeners.get(event_type)
            if listeners and listener in listeners:
                listeners.remove(listener)
                logger.debug(f"Listener '{listener.__name__}' deregistered from event type '{event_type}'.")
                if not listeners:
                    del self._listeners[event_type]
                    logger.debug(f"No more listeners for event type '{event_type}', event type removed.")
            else:
                logger.warning(f"Listener '{listener.__name__}' not found for event type '{event_type}'.")

    def dispatch_event(self, event_type: str, **event_data: Any) -> None:
        """
        Dispatches an event to all registered listeners for the event type.

        Args:
            event_type (str): The type of event being dispatched.
            **event_data: Arbitrary keyword arguments representing event data.
        """
        with self._lock:
            listeners = self._listeners.get(event_type, []).copy()

        if not listeners:
            logger.debug(f"No listeners registered for event type '{event_type}'.")
            return

        logger.debug(f"Dispatching event '{event_type}' to {len(listeners)} listener(s) with data: {event_data}")

        for listener in listeners:
            try:
                listener(**event_data)
                logger.debug(f"Listener '{listener.__name__}' executed successfully for event type '{event_type}'.")
            except Exception as e:
                logger.error(f"Error executing listener '{listener.__name__}' for event type '{event_type}': {e}", exc_info=True)

    def get_registered_event_types(self) -> List[str]:
        """
        Returns a list of event types that have registered listeners.

        Returns:
            List[str]: A list of event type names.
        """
        with self._lock:
            event_types = list(self._listeners.keys())
            logger.debug(f"Currently registered event types: {event_types}")
            return event_types

    def get_listeners(self, event_type: str) -> List[Callable[..., None]]:
        """
        Retrieves the list of listeners registered for a specific event type.

        Args:
            event_type (str): The event type to get listeners for.

        Returns:
            List[Callable[..., None]]: A list of listener functions.
        """
        with self._lock:
            listeners = self._listeners.get(event_type, []).copy()
            logger.debug(f"Retrieved {len(listeners)} listener(s) for event type '{event_type}'.")
            return listeners
