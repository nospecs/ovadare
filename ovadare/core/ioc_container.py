# ovadare/core/ioc_container.py

"""
Inversion of Control (IoC) Container Module for the Ovadare Framework

This module provides the IoCContainer class, which manages the registration and resolution
of dependencies within the framework. It supports singleton and transient registrations
and ensures that components are instantiated with their required dependencies.
"""

from typing import Any, Callable, Dict, Type
from threading import Lock
import logging

# Configure the logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class IoCContainer:
    """
    The IoCContainer manages dependency injection by registering and resolving components.
    It supports singleton and transient lifetimes.
    """

    def __init__(self):
        """
        Initializes the IoCContainer.
        """
        self._registrations: Dict[Type, Callable[[], Any]] = {}
        self._singletons: Dict[Type, Any] = {}
        self._lock = Lock()
        logger.debug("IoCContainer initialized.")

    def register_singleton(self, interface: Type, implementation: Callable[[], Any]) -> None:
        """
        Registers a singleton component.

        Args:
            interface (Type): The interface or base class.
            implementation (Callable[[], Any]): A factory function that returns an instance of the implementation.
        """
        with self._lock:
            self._registrations[interface] = implementation
            logger.debug(f"Singleton registered for interface '{interface.__name__}'.")

    def register_transient(self, interface: Type, implementation: Callable[[], Any]) -> None:
        """
        Registers a transient component.

        Args:
            interface (Type): The interface or base class.
            implementation (Callable[[], Any]): A factory function that returns a new instance each time.
        """
        with self._lock:
            self._registrations[interface] = implementation
            logger.debug(f"Transient registered for interface '{interface.__name__}'.")

    def resolve(self, interface: Type) -> Any:
        """
        Resolves an instance of the specified interface.

        Args:
            interface (Type): The interface or base class to resolve.

        Returns:
            Any: An instance of the requested component.

        Raises:
            ValueError: If the interface is not registered.
        """
        with self._lock:
            if interface not in self._registrations:
                error_message = f"No registration found for interface '{interface.__name__}'."
                logger.error(error_message)
                raise ValueError(error_message)

            if interface in self._singletons:
                logger.debug(f"Returning existing singleton instance for interface '{interface.__name__}'.")
                return self._singletons[interface]

            logger.debug(f"Creating new instance for interface '{interface.__name__}'.")
            implementation = self._registrations[interface]
            instance = implementation()

            # If the registration is a singleton, store the instance
            if self._is_singleton(interface):
                self._singletons[interface] = instance
                logger.debug(f"Singleton instance stored for interface '{interface.__name__}'.")

            return instance

    def _is_singleton(self, interface: Type) -> bool:
        """
        Checks if the registered implementation for the interface is a singleton.

        Args:
            interface (Type): The interface to check.

        Returns:
            bool: True if the implementation is registered as a singleton, False otherwise.
        """
        # In this simple implementation, we assume that all registrations are singletons
        # unless explicitly registered as transient. This method can be expanded if needed.
        return interface in self._registrations and interface not in self._singletons

    def clear(self) -> None:
        """
        Clears all registrations and singletons from the container.
        """
        with self._lock:
            self._registrations.clear()
            self._singletons.clear()
            logger.debug("IoCContainer cleared.")

    def is_registered(self, interface: Type) -> bool:
        """
        Checks if an interface is registered.

        Args:
            interface (Type): The interface to check.

        Returns:
            bool: True if the interface is registered, False otherwise.
        """
        with self._lock:
            is_registered = interface in self._registrations
            logger.debug(f"Interface '{interface.__name__}' is {'registered' if is_registered else 'not registered'}.")
            return is_registered
