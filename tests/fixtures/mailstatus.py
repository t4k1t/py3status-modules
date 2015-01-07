import pytest
import mock
import mailbox


@pytest.fixture
def maildir(tmpdir):
    """Empty maildir fixture."""
    maildir = tmpdir.mkdir("maildir")
    maildir.mkdir("cur")
    maildir.mkdir("new")
    maildir.mkdir("tmp")
    return maildir


@pytest.fixture
def maildir_new_mail(maildir):
    """Maildir fixture containing one unread message."""
    path_string = maildir.dirname + "/" + maildir.basename
    mock_mailbox = mailbox.Maildir(path_string)
    mock_mailbox.add_folder("tmp")
    mock_mailbox.add_folder("cur")
    mock_mailbox.add_folder("new")
    message = mailbox.MaildirMessage()
    mock_mailbox.add(message)
    for m in mock_mailbox.items():
        m[1].set_flags("")
    return maildir


@pytest.fixture
def invalid_maildir(tmpdir):
    """Empty maildir fixture."""
    maildir = tmpdir.mkdir("invalid_maildir")
    return maildir


@pytest.fixture
def read_mailboxes_fixture():
    def read_mailboxes(self, *args, **kwargs):
        self.mboxes = mock.Mock()
        self.mbox_state = 0
        self.unread = 3
    return read_mailboxes


@pytest.fixture
def mailstatus_response_none():
    """Mailstatus response without any unread mails."""
    response = {
        'cached_until': '0000000000.000000',
        'full_text': 'MAIL_TEST: 0',
        'name': 'mailstatus',
    }
    return response


@pytest.fixture
def mailstatus_response_some():
    """Mailstatus response with 3 unread mails."""
    response = {
        'cached_until': '0000000000.000000',
        'color': '#FFFF00',
        'full_text': 'MAIL_TEST: 3',
        'name': 'mailstatus',
    }
    return response


@pytest.fixture
def mailstatus_response_no_mailboxes():
    """Mailstatus response without any configured mailboxes."""
    response = {
        'cached_until': '0000000000.000000',
        'color': '#FF0000',
        'full_text': 'MAIL_TEST: no mailbox configured',
        'name': 'mailstatus',
    }
    return response


__all__ = (
    'maildir',
    'maildir_new_mail',
    'invalid_maildir',
    'read_mailboxes_fixture',
    'mailstatus_response_none',
    'mailstatus_response_some',
    'mailstatus_response_no_mailboxes',
)
