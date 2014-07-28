"""Fixtures common to all modules."""

import pytest


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
def valid_config_path(valid_config):
    """Path to valid config."""
    pathstring = ('{dir}/{base}/modules.ini'.format(
        dir=valid_config.dirname,
        base=valid_config.basename))
    return pathstring


@pytest.fixture
def empty_config(tmpdir):
    """Empty configuration file."""
    tmpdir.join("modules.ini")
    return tmpdir


@pytest.fixture
def i3config():
    """Mock i3config."""
    config = {
        'color_bad': '#FF0000',
        'color_degraded': '#FFFF00',
        'color_good': '#00FF00',
    }
    return config


__all__ = (
    'valid_config',
    'valid_config_path',
    'empty_config',
    'i3config',
)
