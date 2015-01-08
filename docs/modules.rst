.. _modules:

Available Modules
=================

Currently the ``py3status-modules`` collection consists of the modules listed
in this document. Each of these modules can be used separately. Some of them
have to be configured before they work properly - see :ref:`configuration` for
an explanation of the configuration format and an example.


.. _mailstatus_module:

mailstatus
----------

Shows the number of unread mails in all configured mailboxes.

Actions
^^^^^^^

``mailstatus`` does not support any actions at this point.


.. _mpdstatus_module:

mpdstatus
---------

Displays the current song and playback status. Also it enables the user to
pause playback or jump to the previous/next song.

Actions
^^^^^^^

* `Left Click`: Jump to previous song.
* `Middle Click`: Pause/Resume playback.
* `Right Click`: Go to next song.


.. _taskstatus_module:

taskstatus
----------

Shows the number of open tasks. If there are any overdue tasks, the number of
overdue tasks is displayed as well.

Actions
^^^^^^^

``taskstatus`` does not support any actions at this point.


.. _batterystatus_module:

batterystatus
-------------

Indicates the current battery status in a configurable format.

Actions
^^^^^^^

``batterystatus`` does not support any actions at this point.


.. _alsastatus_module:

alsastatus
----------

Prints the current ALSA volume for a configurable mixer.

Actions
^^^^^^^

* `Middle Click`: Mute/Unmute mixer.
