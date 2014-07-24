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
    def test_incorrect_password(self, mock_client):
        """Test Data initialisation with incorrect password."""
        data = None
        with pytest.raises(MPDstatusException) as e:
            data = Data('localhost', 6600, "")
        assert "incorrect password" in str(e).lower()
        assert data is None
