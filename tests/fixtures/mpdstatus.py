"""Fixtures for the ``mpdstatus`` module."""

import pytest


@pytest.fixture
def current_song():
    """Mock current_song method of MPD client class."""
    def cur(*args, **kwargs):
        return {
            'artist': 'Best Artist',
            'title': 'Best Song',
        }
    return cur


@pytest.fixture
def mpd_state_play():
    """Mock MPD state `play`"""
    def state(*args, **kwargs):
        return {
            'state': 'play',
        }
    return state


@pytest.fixture
def mpd_state_pause():
    """Mock MPD state `pause`"""
    def state(*args, **kwargs):
        return {
            'state': 'pause',
        }
    return state


@pytest.fixture
def mpd_state_stop():
    """Mock MPD state `stop`"""
    def state(*args, **kwargs):
        return {
            'state': 'stop',
        }
    return state


@pytest.fixture
def mpdstatus_response_disconnected():
    """MPDstatus response on disconnected MPD."""
    response = {
        'cached_until': '0000000000.000000',
        'color': '#FF0000',
        'full_text': 'MPD_TEST: not connected',
        'name': 'mpdstatus',
    }
    return response


@pytest.fixture
def mpdstatus_response_playing():
    """MPDstatus response on playing MPD."""
    response = {
        'cached_until': '0000000000.000000',
        'color': '#00FF00',
        'full_text': 'MPD_TEST: Best Artist - Best Song',
        'name': 'mpdstatus',
    }
    return response


@pytest.fixture
def mpdstatus_response_paused():
    """MPDstatus response on paused MPD."""
    response = {
        'cached_until': '0000000000.000000',
        'color': '#FFFF00',
        'full_text': 'MPD_TEST: Best Artist - Best Song',
        'name': 'mpdstatus',
    }
    return response


@pytest.fixture
def mpdstatus_response_stopped():
    """MPDstatus response on stopped MPD."""
    response = {
        'cached_until': '0000000000.000000',
        'full_text': 'MPD_TEST: Best Artist - Best Song',
        'name': 'mpdstatus',
    }
    return response


__all__ = (
    'current_song',
    'mpd_state_play',
    'mpd_state_pause',
    'mpd_state_stop',
    'mpdstatus_response_disconnected',
    'mpdstatus_response_playing',
    'mpdstatus_response_paused',
    'mpdstatus_response_stopped',
)
