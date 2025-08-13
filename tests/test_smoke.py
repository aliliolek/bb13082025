"""Smoke tests for the sample application."""

from src.app import main


def test_main_callable() -> None:
    """Ensure main function is callable."""
    assert callable(main.main)
