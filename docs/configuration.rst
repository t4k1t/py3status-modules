.. _configuration:

Configuration
-------------

Since ``py3status-modules 0.3.0`` and ``py3status 2.0`` you can simply
configure these modules via your ``i3status.conf``.


common settings
"""""""""""""""

Some basic settings can be configured for any module:

``name``
   Title that is shown in front of the actual data. For example ``MAIL`` for
   the ``mailstatus`` module.

``cache_timeout``
   Refresh interval in seconds.

``error_timeout``
   Time after which error messages are cleared from the output in seconds.

.. _mailstatus_settings:

mailstatus settings
"""""""""""""""""""

``mailboxes``
   Space-separated list of paths to the mailboxes that should be monitored by
   ``mailstatus``. At this time only the ``Maildir`` format is supported.

   .. note::

      ``mailstatus`` uses shell-like syntax for these paths. So whitespaces in
      paths, for example, need to be escaped with a backslash.

Example
'''''''

The following example will:

* Display ``✉`` as title
* Update the mail count every ``10`` seconds
* Read the following two mailboxes:
   #. ``~/.mail/local``
   #. ``~/.mail/My Gmail Mailbox/Inbox``


.. code-block:: bash

   mailstatus {
           name = "✉"
           cache_timeout = 10
           mailboxes = "~/.mail/local ~/.mail/My\ Gmail\ Mailbox/Inbox"
   }


taskstatus settings
"""""""""""""""""""

``taskstatus`` currently does not support any dedicated settings.

Example
'''''''

The following example will:

* Display ``✓`` as title
* Update it's output every ``10`` seconds

.. code-block:: bash

   taskstatus {
           name = "✓"
           cache_timeout = 10
   }


mpdstatus settings
""""""""""""""""""

``host``
   Hostname or IP of the computer MPD is running on. **Defaults to
   ``localhost``**

``port``
   Port MPD is listening on. **Per default 6600**

``password``
   If you set up your MPD to use a password you can set it here.

``max_length``
   Crop output to this number of characters. **No cropping per default**

``hide_on_pause``
   If set to `true` normal output will be suppressed on pause and only the
   module ``name`` (per default ``♬``) will be displayed in order to maintain
   mouse controls in the status bar. ``mpdstatus``' output will be hidden until
   playback is unpaused again.

Example
'''''''

The following example will:

* Display ``♬`` as title
* Update ``mpdstatus'`` output on every ``i3status`` refresh
* Connect to the host ``mympdserver``
* on Port ``6600``
* using the password ``correcthorsebatterystaple``
* Enable the ``hide_on_pause`` feature

.. code-block:: bash

   mpdstatus {
           name = "♬"
           cache_timeout = 0
           host = "localhost"
           port = 6600
           password = "correcthorsebatterystaple"
           hide_on_pause = true
   }


.. _batterystatus_settings:

batterystatus settings
""""""""""""""""""""""

``threshold``
   Percentage value below which the output of ``batterystatus`` will turn red.

``format``
   Output format. Possible values:

      * `%bar`        Bar representation of current charge
      * `%percentage` Current charge in percent
      * `%time`       Remaining time (until empty/full)
      * `%state`      Battery state (charing, discharging, full)

   Any of these values can be combined in any way. See :ref:`example_config`
   for another example.

Example
'''''''

The following example will:

* Display ``⚡`` as title
* Update the output every ``30`` seconds
* Set the warning threshold to ``15`` percent
* Set the output format string to print a ``bar representation of the battery's
  current charge``, followed by it's ``charge in percent``.

.. code-block:: bash

   batterystatus {
           name = "⚡"
           cache_timeout = 30
           threshold = 15
           format = "%bar %percentage%"
   }


alsastatus settings
"""""""""""""""""""

``mixer``
   Specifies which mixer should be queried for data / controlled. **Defaults
   to ``Master``**

``indicator``
   Symbol which indicates that the mixer is currently muted. **Defaults to
   ``[M]``**

``step``
   Stepsize by which to decrease/increase volume. **Defaults to 3**

Example
'''''''

The following example will:

* Display ``♪`` as title
* Update the output on every ``i3status`` refresh
* Set the mute indicator to ``[M]``

.. code-block:: bash

   alsastatus {
           name = "♪"
           cache_timeout = 0
           indicator = "[M]"
           step = 3
   }


.. _example_config:

Example config
""""""""""""""

This example config shows how your ``i3status.conf`` could look like.

.. note::

   ``run_watch`` and ``load`` are vanilla i3status modules

.. literalinclude:: examples/i3status.conf.example
   :language: bash

.. seealso::

   `Loading a py3status module
   <https://github.com/ultrabug/py3status/wiki/Load-and-order-py3status-modules-directly-from-your-current-i3status-config#loading-a-py3status-module>`_
   from py3status' documentation.

