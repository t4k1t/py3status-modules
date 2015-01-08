=================
py3status-modules
=================

|docs|

Collection of modules for py3status_.

dependencies
============

- python (>=3.2)
- py3status (>=2.0)

- task (>=2.1.2) ``taskstatus``
- python-mpd (>=0.5.1) ``mpdstatus``
- upower (>=0.9.23) ``batterystatus``
- dbus-python (>=1.2.0) ``batterystatus``
- alsa-utils (>=1.0.28) ``alsastatus``


modules
=======

- ``mailstatus`` shows the number of unread mails in your mailboxes. Currently
  only suports `Maildir` format.

- ``taskstatus`` shows open Taskwarrior_ tasks. If you have overdue tasks it also
  displays the number of overdue tasks and changes color.

- ``mpdstatus`` connects to MPD_ and shows the currently playing song. Left click
  will go to the previous song, right click will jump to the next song and
  middle click will pause playback.

- ``batterystatus`` shows the status of your battery as reported by upower. For
  upower support batterystatus uses slightly modified code of the batti_
  project.

- ``alsastatus`` shows the current volume of a configurable ALSA_ mixer. Also, middle
  click will mute/unmute said mixer.


configuration
=============

Since py3status-modules 0.3.0 you can configure each module directly in your `i3status.conf`.

See `the configuration section of py3status-modules' documentation
<https://py3status-modules.readthedocs.org/en/latest/configuration.html>`_ for
an explanation and examples.


documentation
=============

You can find detailed documentation at
`py3status-modules' Read the Docs page
<https://py3status-modules.readthedocs.org/en/latest/>`_, powered by Sphinx_.


.. _MPD: http://www.musicpd.org/
.. _py3status: https://github.com/ultrabug/py3status
.. _Taskwarrior: http://taskwarrior.org/
.. _batti: https://code.google.com/p/batti-gtk/
.. _Sphinx: http://sphinx-doc.org
.. _ALSA: http://www.alsa-project.org/
 
.. |docs| image:: https://readthedocs.org/projects/py3status-modules/badge/?version=latest
   :alt: Documentation status
   :scale: 100%
   :target: https://py3status-modules.readthedocs.org/en/latest/
