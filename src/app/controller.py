"""Application-level business logic."""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class AppController:
    """Encapsulates simple application state.

    The controller exposes methods that can be triggered from the Telegram bot
    handlers. In a real application this would coordinate services and contain
    the business rules.
    """

    def __init__(self) -> None:
        self._running = False

    def start(self) -> str:
        """Start the application."""
        if not self._running:
            self._running = True
            logger.info("Application started")
            return "Application started."
        logger.info("Start requested while already running")
        return "Application is already running."

    def stop(self) -> str:
        """Stop the application."""
        if self._running:
            self._running = False
            logger.info("Application stopped")
            return "Application stopped."
        logger.info("Stop requested while not running")
        return "Application is not running."

    def status(self) -> str:
        """Return the running status."""
        return "Application is running." if self._running else "Application is stopped."
