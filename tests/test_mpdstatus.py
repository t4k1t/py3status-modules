"""Tests for the mpdstatus module."""

import pytest
import mock


MPD = False

try:
    import mpd
except ImportError:
    pass
else:
    from mpdstatus.mpdstatus import Data, MPDstatusException
    MPD = True


def command_error(*args, **kwargs):
    """Raise CommandError with specific error message."""
    raise mpd.CommandError("Incorrect password.")


@pytest.mark.skipif(not MPD, reason="requires python-mpd2")
class TestData:
    """Test Data class."""

    @mock.patch('mpd.MPDClient.connect', side_effect=command_error)
    def test_incorrect_password(self, mock_connection):
        """Test Data initialisation with incorrect password."""
        data = None
        with pytest.raises(MPDstatusException) as e:
            data = Data('', 6600, "", None)
        assert "incorrect password" in str(e)
        assert data is None

    @mock.patch('mpd.MPDClient.status')
    @mock.patch('mpd.MPDClient.connect')
    def test_connection(self, mock_connection, mock_status):
        """Test MPD connection check."""
        data = None
        data = Data('', 6600, "", None)
        assert data.has_connection() is True

        mock_status.side_effect = Exception
        assert data.has_connection() is False

    @mock.patch('mpd.MPDClient.connect')
    @mock.patch('mpd.MPDClient.pause')
    @mock.patch('mpd.MPDClient.next')
    @mock.patch('mpd.MPDClient.previous')
    def test_controls(self, mock_prev, mock_next, mock_pause, mock_connection):
        """Check control commands."""
        data = None
        data = Data('', 6600, "", None)

        data.previous()
        data.next()
        data.pause()
        assert data is not None

    @mock.patch('mpd.MPDClient.connect')
    def test_controls_fail(self, mock_connection):
        """Check control commands without MPD connection."""
        data = None
        data = Data('', 6600, "", None)

        with pytest.raises(mpd.ConnectionError):
            data.previous()
        with pytest.raises(mpd.ConnectionError):
            data.next()
        with pytest.raises(mpd.ConnectionError):
            data.pause()
        assert data is not None

    @mock.patch('mpd.MPDClient.connect')
    def test_reconnect_fail(self, mock_connection):
        """Check reconnecting without MPD connection."""
        data = None
        data = Data('', 6600, "", None)
        assert data is not None

        data.reconnect()
        assert data.has_connection() is False

    @mock.patch('mpd.MPDClient')
    @mock.patch('mpd.MPDClient.connect')
    def test_get_state(self, mock_connect, mock_client, current_song,
                       mpd_state_play):
        """Test playback information retrieval."""
        data = None
        data = Data('', 6600, "", None)
        data.client = mock.Mock(currentsong=current_song,
                                status=mpd_state_play)
        artist, title, state = data.get_stats()
        assert artist == "Best Artist"
        assert title == "Best Song"
        assert state == "play"
