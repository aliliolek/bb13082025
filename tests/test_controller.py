"""Tests for the AppController class."""

from __future__ import annotations

import asyncio

from src.app.controller import AppController, AppState


class DummyClient:
    """Lightweight stub for ``BybitP2PClient`` used in tests."""

    def get_latest_order(self) -> None:  # pragma: no cover - no logic needed
        return None


def test_start_and_status() -> None:
    async def run() -> None:
        controller = AppController(DummyClient())
        assert controller.status().state == AppState.STOPPED

        start_status = controller.start()
        assert start_status.state == AppState.RUNNING
        assert len(start_status.tasks) == 1

        duplicate_status = controller.start()
        assert duplicate_status.state == AppState.RUNNING
        assert len(duplicate_status.tasks) == 1

        stop_status = controller.stop()
        await asyncio.sleep(0)  # allow cancelled tasks to finish
        assert stop_status.state == AppState.STOPPED

    asyncio.run(run())


def test_stop() -> None:
    async def run() -> None:
        controller = AppController(DummyClient())
        controller.start()
        stop_status = controller.stop()
        await asyncio.sleep(0)
        assert stop_status.state == AppState.STOPPED
        assert controller.status().tasks == ()

    asyncio.run(run())
