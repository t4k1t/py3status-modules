"""Tests for the mailstatus module."""

import pytest
from mailstatus.mailstatus import Data, MailstatusException


class TestData:

    """Test Data functions."""

    def test_maildir_unread(self, maildir_new_mail):
        """Test malidir with one unread mail."""
        path_string = (maildir_new_mail.dirname + "/" +
                       maildir_new_mail.basename)
        data = Data([path_string])
        unread = data.get_unread()
        assert unread == 1
        # Esoteric test of access time check.
        unread = data.get_unread()
        assert unread == 1

    def test_maildir_no_unread(self, maildir):
        """Test malidir without unread mails."""
        path_string = maildir.dirname + "/" + maildir.basename
        data = Data([path_string])
        unread = data.get_unread()
        assert unread == 0

    def test_invalid_maildir(self, invalid_maildir):
        """Test invalid maildir."""
        path_string = invalid_maildir.dirname + "/" + invalid_maildir.basename
        # Correct path but invalid maildir.
        with pytest.raises(MailstatusException) as e:
            Data([path_string])
        assert "invalid maildir" in str(e)

        # Invalid path.
        with pytest.raises(MailstatusException) as e:
            Data(["This path should not exist"])
        assert "invalid path" in str(e)
