=================
py3status-modules
=================

Collection of modules for py3status.

These modules will need python3 to work.


modules
=======

- **mailstatus** operates in two modes
    - **unread** mode shows number of unread mails.
    - **subject** mode shows subject of the unread mails. A right click will show
        the subject of the next email.

- **taskstatus** shows open Taskwarrior_ tasks. If you have overdue tasks it also
      displays the number of overdue tasks and changes color.


configuration
=============

You can configure each module in `~/.i3/py3status/modules.cfg`::

    [mailstatus]
    # title
    #title = '✉' # slightly fancier title
    # where to put module output (can be between stock i3status ones)
    order = 0
    # refresh interval in seconds
    interval = 0
    # list of mailboxes in quotes, separated by whitespace
    #mailboxes = '/path/to/mailbox' '/path/to/another/mailbox'

    [taskstatus]
    #title = '✓'
    order = 1
    interval = 120

.. _Taskwarrior: http://taskwarrior.org/
