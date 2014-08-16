.. _configuration:

Configuration
-------------

``py3status-modules`` will look for a configuration file in
``~/.i3/py3status/modules.ini``.


Config format
^^^^^^^^^^^^^

Every module has its own section in the configuration. For example the
``mailstatus`` module will only read the ``[mailstatus]`` section of the
config.

.. code-block:: ini

    [mailstatus]
    title     = TITLE
    order     = POSITION_IN_BAR
    interval  = REFRESH_INTERVAL
    mailboxes = MAILBOX_PATHS

    [taskstatus]
    title     = TITLE
    order     = POSITION_IN_BAR
    interval  = REFRESH_INTERVAL

    [mpdstatus]
    title     = TITLE
    order     = POSITION_IN_BAR
    interval  = REFRESH_INTERVAL
    host      = MPD_HOST
    port      = MPD_PORT
    password  = MPD_PASSWORD

    [batterystatus]
    title     = TITLE
    order     = POSITION_IN_BAR
    interval  = REFRESH_INTERVAL
    threshold = WARNING_THRESHOLD
    format    = OUTPUT_FORMAT


common settings
"""""""""""""""

Some basic settings can be configured for any module:

``title``
   Title that is shown in front of the actual data. For example ``MAIL`` for
   the ``mailstatus`` module.

``order``
   Sets the position of the module in the py3status bar. A value of ``0`` for
   example would place the module on the far left.

``interval``
   Refresh interval in seconds.


mailstatus section
""""""""""""""""""

``mailboxes``
   Space-separated list of paths to the mailboxes that should be monitored by
   ``mailstatus``. At this time only the ``Maildir`` format is supported.


taskstatus section
""""""""""""""""""

``taskstatus`` currently does not support any configuration.


mpdstatus section
"""""""""""""""""

``host``
   Hostname or IP of the computer MPD is running on. **Defaults to
   ``localhost``**

``port``
   Port MPD is listening on. **Per default 6600**

``password``
   If you set up your MPD to use a password you can set it here.


batterystatus section
"""""""""""""""""""""

``threshold``
   Percentage value below which the output of ``batterystatus`` will turn red.

``format``
   Output format. Possible values:

      * `{bar}`        Bar representation of current charge
      * `{percentage}` Current charge in percent
      * `{time}`       Remaining time (until empty/full)
      * `{state}`      Battery state (charing, discharging, full)

   Any of these values can be combined in any way. See :ref:`example_config`
   for an example.


.. _example_config:

Example config
^^^^^^^^^^^^^^

.. literalinclude:: examples/modules.ini.example
   :language: ini
