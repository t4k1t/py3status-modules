"""Tests for the mpdstatus module."""

import pytest
import mock
import os


MPD = False

try:
    import mpd
except ImportError:
    pass
else:
    from mpdstatus.mpdstatus import Data, MPDstatusException, Py3status
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
            data = Data('', 6600, "")
        assert "incorrect password" in str(e)
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
    def test_controls(self, mock_prev, mock_next, mock_pause, mock_connection):
        """Check control commands."""
        data = None
        data = Data('', 6600, "")

        data.previous()
        data.next()
        data.pause()
        assert data is not None

    @mock.patch('mpd.MPDClient.connect')
    def test_controls_fail(self, mock_connection):
        """Check control commands without MPD connection."""
        data = None
        data = Data('', 6600, "")

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
        data = Data('', 6600, "")
        assert data is not None

        data.reconnect()
        assert data.has_connection() is False

    @mock.patch('mpd.MPDClient')
    @mock.patch('mpd.MPDClient.connect')
    def test_get_state(self, mock_connect, mock_client, current_song,
                 mpd_state_play):
        """Test playback information retrieval."""
        data = None
        data = Data('', 6600, "")
        data.client = mock.Mock(currentsong=current_song,
                                status=mpd_state_play)
        artist, title, state = data.get_stats()
        assert artist == "Best Artist"
        assert title == "Best Song"
        assert state == "play"


@pytest.mark.skipif(not MPD, reason="requires python-mpd2")
class TestResponse:

    """Test Py3status class."""

    @mock.patch('mpd.MPDClient')
    @mock.patch('mpd.MPDClient.connect')
    def test_empty_config(self, mock_connect, mock_client, monkeypatch,
                          empty_config, i3config):
        """Test config without mpdstatus section."""
        def mockreturn(path):
            path_string = (empty_config.dirname + "/" +
                           empty_config.basename + "/modules.ini")
            return path_string
        monkeypatch.setattr(os.path, 'expanduser', mockreturn)

        py3status = Py3status()
        assert py3status is not None

    @mock.patch('mpd.MPDClient')
    @mock.patch('mpd.MPDClient.connect')
    def test_valid_config(self, mock_connect, mock_client, monkeypatch,
                        valid_config_path, i3config,
                        mpdstatus_response_disconnected):
        """Test valid config."""
        monkeypatch.setattr(os.path, 'expanduser', lambda x:
                            valid_config_path)
        reference = mpdstatus_response_disconnected

        py3status = Py3status()
        module = py3status.mpdstatus(mock.Mock(), i3config)
        assert module[1]['color'] == reference['color']
        assert module[1]['full_text'] == reference['full_text']
        assert module[1]['name'] == reference['name']

    @mock.patch('mpd.MPDClient')
    @mock.patch('mpd.MPDClient.connect')
    def test_playing(self, mock_connect, mock_client, current_song,
                     mpd_state_play, monkeypatch, valid_config_path, i3config,
                     mpdstatus_response_playing):
        """Test playback response with running MPD."""
        monkeypatch.setattr(os.path, 'expanduser', lambda x:
                            valid_config_path)
        reference = mpdstatus_response_playing

        py3status = Py3status()
        py3status.data.client = mock.Mock(currentsong=current_song,
                                          status=mpd_state_play)
        module = py3status.mpdstatus(mock.Mock(), i3config)
        assert module[1]['color'] == reference['color']
        assert module[1]['full_text'] == reference['full_text']
        assert module[1]['name'] == reference['name']

    @mock.patch('mpd.MPDClient')
    @mock.patch('mpd.MPDClient.connect')
    def test_paused(self, mock_connect, mock_client, current_song,
                    mpd_state_pause, monkeypatch, valid_config_path, i3config,
                    mpdstatus_response_paused):
        """Test playback response with paused MPD."""
        monkeypatch.setattr(os.path, 'expanduser', lambda x:
                            valid_config_path)
        reference = mpdstatus_response_paused

        py3status = Py3status()
        py3status.data.client = mock.Mock(currentsong=current_song,
                                          status=mpd_state_pause)
        module = py3status.mpdstatus(mock.Mock(), i3config)
        assert module[1]['color'] == reference['color']
        assert module[1]['full_text'] == reference['full_text']
        assert module[1]['name'] == reference['name']

    @mock.patch('mpd.MPDClient')
    @mock.patch('mpd.MPDClient.connect')
    def test_stopped(self, mock_connect, mock_client, current_song,
                     mpd_state_stop, monkeypatch, valid_config_path, i3config,
                     mpdstatus_response_stopped):
        """Test playback response with stopped playback."""
        monkeypatch.setattr(os.path, 'expanduser', lambda x:
                            valid_config_path)
        reference = mpdstatus_response_stopped

        py3status = Py3status()
        py3status.data.client = mock.Mock(currentsong=current_song,
                                          status=mpd_state_stop)
        module = py3status.mpdstatus(mock.Mock(), i3config)
        assert 'color' not in module[1]
        assert module[1]['full_text'] == reference['full_text']
        assert module[1]['name'] == reference['name']
