"""Tests for the mpdstatus module."""

import pytest
import mock
import mpd

from mpdstatus.mpdstatus import Data, MPDstatusException
# TODO: Properly test Data class.
# TODO: Test actual py3status response.


def command_error(*args, **kwargs):
    """Raise CommandError with specific error message."""
    raise mpd.CommandError("Incorrect password.")


class TestData:

    """Test Data class."""

    @mock.patch('mpd.MPDClient.connect', side_effect=command_error)
    def test_incorrect_password(self, mock_connection):
        """Test Data initialisation with incorrect password."""
        data = None
        with pytest.raises(MPDstatusException) as e:
            data = Data('', 6600, "")
        assert "incorrect password" in str(e).lower()
        assert data is None

    @mock.patch('mpd.MPDClient.status')
    @mock.patch('mpd.MPDClient.connect')
    def test_connection(self, mock_connection, mock_status):
        """Test MPD connection check."""
        data = None
        data = Data('', 6600, "")
        assert data.has_connection() is True

        mock_status.side_effect = Exception
        assert data.has_connection() is False

    @mock.patch('mpd.MPDClient.connect')
    @mock.patch('mpd.MPDClient.pause')
    @mock.patch('mpd.MPDClient.next')
    @mock.patch('mpd.MPDClient.previous')
    def test_controls_fail(self, mock_prev, mock_next, mock_pause, mock_connection):
        """Check control commands without MPD connection."""
        data = None
        data = Data('', 6600, "")

        data.previous()
        data.next()
        data.pause()
        assert data is not None
