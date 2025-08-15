"""Application-level business logic and task management."""

from __future__ import annotations

import asyncio
import logging
import os
from dataclasses import dataclass
from enum import Enum
from typing import Dict

from .api_client import BybitP2PClient

logger = logging.getLogger(__name__)


class AppState(Enum):
    """Represents the running state of the application."""

    RUNNING = "running"
    STOPPED = "stopped"


@dataclass(frozen=True)
class ControllerStatus:
    """Structured status response returned by controller methods."""

    state: AppState
    tasks: tuple[str, ...]


class AppController:
    """Coordinate background tasks and the Bybit P2P client."""

    _DEFAULT_POLL_INTERVAL = 60.0

    def __init__(self, client: BybitP2PClient, *, poll_interval: float | None = None) -> None:
        self._client = client
        self._tasks: Dict[str, asyncio.Task] = {}

        if poll_interval is None:
            interval_env = os.getenv("APP_POLL_INTERVAL")
            if interval_env is None:
                poll_interval = self._DEFAULT_POLL_INTERVAL
            else:
                poll_interval = float(interval_env)
        self._poll_interval = poll_interval

    # ------------------------------------------------------------------
    # Task management helpers
    # ------------------------------------------------------------------
    async def _poll_orders(self) -> None:
        """Periodically poll the latest order.

        The loop runs until cancelled. It intentionally swallows the
        ``CancelledError`` so that cancellation is clean and silent.
        """

        try:
            while True:
                try:
                    self._client.get_latest_order()
                except Exception:  # pragma: no cover - client errors logged
                    logger.exception("Error polling latest order")
                await asyncio.sleep(self._poll_interval)
        except asyncio.CancelledError:
            logger.info("Polling task cancelled")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def start(self) -> ControllerStatus:
        """Start background tasks if not already running."""

        if self._tasks:
            logger.info("Start requested but tasks already running")
            return self.status()

        loop = asyncio.get_running_loop()
        self._tasks["order_polling"] = loop.create_task(self._poll_orders())
        logger.info("Application started with %d task(s)", len(self._tasks))
        return self.status()

    def stop(self) -> ControllerStatus:
        """Cancel all running tasks."""

        if not self._tasks:
            logger.info("Stop requested but no running tasks")
            return self.status()

        tasks = list(self._tasks.values())
        for task in tasks:
            task.cancel()

        self._tasks.clear()
        asyncio.get_running_loop().create_task(self._await_tasks(tasks))
        logger.info("Application stopped")
        return self.status()

    async def _await_tasks(self, tasks: list[asyncio.Task]) -> None:
        """Wait for a collection of tasks to finish."""

        await asyncio.gather(*tasks, return_exceptions=True)

    def status(self) -> ControllerStatus:
        """Return the current controller status."""

        state = AppState.RUNNING if self._tasks else AppState.STOPPED
        return ControllerStatus(state=state, tasks=tuple(self._tasks.keys()))
