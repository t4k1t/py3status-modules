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
title = MAIL_TEST:
mailboxes = '%s'

[taskstatus]
order = 1
interval = 120

[mpdstatus]
order = 2
title = MPD_TEST:
host =

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
    """Configuration without mailboxes key."""
    f = tmpdir.join("modules.ini")
    f.write("""
[mailstatus]
title = ✉
""")
    return tmpdir


@pytest.fixture
def config_empty_mailboxes(tmpdir):
    """Configuration without any mailboxes."""
    f = tmpdir.join("modules.ini")
    f.write("""
[mailstatus]
title = ✉
mailboxes =
""")
    return tmpdir


@pytest.fixture
def empty_config(tmpdir):
    """Empty configuration file."""
    tmpdir.join("modules.ini")
    return tmpdir


@pytest.fixture
def config_no_mailboxes_path(config_no_mailboxes):
    """Path to configuration without mailboxes key ."""
    pathstring = ('{dir}/{base}/modules.ini'.format(
        dir=config_no_mailboxes.dirname,
        base=config_no_mailboxes.basename))
    return pathstring


@pytest.fixture
def valid_config_path(valid_config):
    """Path to valid config."""
    pathstring = ('{dir}/{base}/modules.ini'.format(
        dir=valid_config.dirname,
        base=valid_config.basename))
    return pathstring


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
def i3config():
    """Mock i3config."""
    config = {
        'color_bad': '#FF0000',
        'color_degraded': '#FFFF00',
        'color_good': '#00FF00',
    }
    return config


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
