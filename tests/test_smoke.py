"""Smoke tests for the sample application."""

import main


def test_main_callable() -> None:
    """Ensure main function is callable."""
    assert callable(main.main)
