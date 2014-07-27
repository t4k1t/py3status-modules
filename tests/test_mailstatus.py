"""Tests for the mailstatus module."""

import pytest
import mock
import os.path
from mailstatus.mailstatus import Data, Py3status, MailstatusException


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


class TestResponse:

    """Test Py3status class."""

    def test_config_no_mailboxes(self, monkeypatch, config_no_mailboxes):
        """Test config with mailstatus section but no mailboxes."""
        def mockreturn(path):
            path_string = (config_no_mailboxes.dirname + "/" +
                           config_no_mailboxes.basename + "/modules.ini")
            return path_string
        monkeypatch.setattr(os.path, 'expanduser', mockreturn)
        with pytest.raises(MailstatusException) as e:
            Py3status()
        assert "no mailboxes" in str(e)

    def test_empty_config(self, monkeypatch, empty_config):
        """Test config without mailstatus section."""
        def mockreturn(path):
            path_string = (empty_config.dirname + "/" +
                           empty_config.basename + "/modules.ini")
            return path_string
        monkeypatch.setattr(os.path, 'expanduser', mockreturn)
        with pytest.raises(MailstatusException) as e:
            Py3status()
        assert "no mailstatus section" in str(e)

    def test_empty_mailboxes(self, monkeypatch, config_empty_mailboxes):
        """Test config with empty mailboxes setting."""
        def mockreturn(path):
            path_string = (config_empty_mailboxes.dirname + "/" +
                           config_empty_mailboxes.basename + "/modules.ini")
            return path_string
        monkeypatch.setattr(os.path, 'expanduser', mockreturn)
        py3 = Py3status()
        unread = py3.data.get_unread()
        assert 'no mailbox' in unread

    @mock.patch('mailstatus.mailstatus.Data.read_mailboxes')
    def test_no_mails(self, mock_mailboxes, monkeypatch, valid_config_path,
                      i3config, mailstatus_response_none):
        """Test response without any unread mails."""
        monkeypatch.setattr(os.path, 'expanduser', lambda x:
                            valid_config_path)
        reference = mailstatus_response_none
        def fun(*args, **kwargs):
            self.mboxes = 0
            self.mbox_state = 0
            self.unread = 0
            return

        py3status = Py3status()
        py3status.data = mock.Mock(read_mailboxes=fun, get_unread=lambda: 0)
        module = py3status.mailstatus(mock.Mock(), i3config)
        assert 'color' not in module[1]
        assert module[1]['full_text'] == reference['full_text']
        assert module[1]['name'] == reference['name']

    @mock.patch('mailstatus.mailstatus.Data.read_mailboxes')
    def test_some_mails(self, mock_mailboxes, monkeypatch, valid_config_path,
                        i3config, mailstatus_response_some):
        """Test response with some unread mails."""
        monkeypatch.setattr(os.path, 'expanduser', lambda x:
                            valid_config_path)
        reference = mailstatus_response_some
        def fun(*args, **kwargs):
            self.mboxes = mock.Mock()
            self.mbox_state = 0
            self.unread = 3
            return

        py3status = Py3status()
        py3status.data = mock.Mock(read_mailboxes=fun, get_unread=lambda: 3)
        module = py3status.mailstatus(mock.Mock(), i3config)
        assert module[1]['color'] == reference['color']
        assert module[1]['full_text'] == reference['full_text']
        assert module[1]['name'] == reference['name']

    @mock.patch('mailstatus.mailstatus.Data.read_mailboxes')
    def test_no_mailboxes(self, mock_mailboxes, monkeypatch,
                          config_no_mailboxes_path, i3config,
                          mailstatus_response_no_mailboxes):
        """Test response with no mailboxes configured."""
        monkeypatch.setattr(os.path, 'expanduser', lambda x:
                            config_no_mailboxes_path)
        reference = mailstatus_response_no_mailboxes
        def fun(*args, **kwargs):
            self.mboxes = mock.Mock()
            self.mbox_state = 0
            self.unread = 3
            return

        with pytest.raises(MailstatusException) as e:
            py3status = Py3status()
        assert "no mailboxes configured" in str(e)
