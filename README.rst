=================
py3status-modules
=================

Collection of modules for py3status_.

dependencies
============

python (>=3.2)
py3status (>=1.1)
python-mpd (>=0.5.1) *mpdstatus*


modules
=======

- mailstatus operates in two modes
    - unread mode shows number of unread mails.
    - subject mode shows subject of the unread mails. A right click will show
      the subject of the next email.

- taskstatus shows open Taskwarrior_ tasks. If you have overdue tasks it also
  displays the number of overdue tasks and changes color.

- mpdstatus connects to MPD_ and shows the currently playing song. Left click
  will go to the previous song, right click will jump to the next song and
  middle click will pause playback.


configuration
=============

You can configure each module in `~/.i3/py3status/modules.ini`::

    [mailstatus]
    ;title = '✉'
    ; where to put module output (can be between stock i3status ones)
    order = 0
    ; refresh interval in seconds
    interval = 0
    ; list of mailboxes in quotes, separated by whitespace
    ;mailboxes = '/path/to/mailbox' '/path/to/another/mailbox'

    [taskstatus]
    ;title = '✓'
    order = 1
    interval = 120

    [mpdstatus]
    ;title = '♬'
    order = 2
    interval = 0
    ;host = 'localhost'
    ;port = 6600

.. _MPD: http://www.musicpd.org/
.. _py3status: https://github.com/ultrabug/py3status
.. _Taskwarrior: http://taskwarrior.org/
