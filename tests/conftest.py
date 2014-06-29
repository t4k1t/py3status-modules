import pytest
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
def valid_config(tmpdir, maildir):
    """Valid configuration."""
    path_string = maildir.dirname + "/" + maildir.basename
    f = tmpdir.join("modules.ini")
    f.write("""
[mailstatus]
order = 0
mailboxes = '%s'

[taskstatus]
order = 1
interval = 120

[mpdstatus]
order = 2

[batterystatus]
order = 9
interval = 2
threshold = 15
format = {bar} {percentage}%% {time}
""" % path_string)
    return tmpdir


@pytest.fixture
def invalid_maildir(tmpdir):
    """Empty maildir fixture."""
    maildir = tmpdir.mkdir("invalid_maildir")
    return maildir


@pytest.fixture
def config_no_mailboxes(tmpdir):
    """Invalid configuration."""
    f = tmpdir.join("modules.ini")
    f.write("""
[mailstatus]
title = ✉
""")
    return tmpdir


@pytest.fixture
def config_empty_mailboxes(tmpdir):
    """Invalid configuration."""
    f = tmpdir.join("modules.ini")
    f.write("""
[mailstatus]
title = ✉
mailboxes =
""")
    return tmpdir


@pytest.fixture
def empty_config(tmpdir):
    """Invalid configuration."""
    tmpdir.join("modules.ini")
    return tmpdir
