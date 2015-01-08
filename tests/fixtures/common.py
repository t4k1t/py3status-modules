"""Fixtures common to all modules."""

import pytest


@pytest.fixture
def i3config():
    """Mock i3config."""
    config = {
        'color_bad': '#FF0000',
        'color_degraded': '#FFFF00',
        'color_good': '#00FF00',
    }
    return config


__all__ = (
    'i3config',
)
