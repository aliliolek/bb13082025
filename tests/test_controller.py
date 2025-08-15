"""Tests for the AppController class."""

from src.app.controller import AppController


def test_start_and_status() -> None:
    controller = AppController()
    assert controller.status() == "Application is stopped."
    assert controller.start() == "Application started."
    assert controller.status() == "Application is running."


def test_stop() -> None:
    controller = AppController()
    controller.start()
    assert controller.stop() == "Application stopped."
    assert controller.status() == "Application is stopped."
