.. _changelog:

Changelog
=========

0.4.0
-----

* Add config validation to all modules.

* Add better error handling mechanism to all modules.

* `alsastatus`: Make ``stepsize`` configurable.

* `mpdstatus`: Fix output on unknown song title.


0.3.0
-----

* **py3status-modules now depends on py3status >= 2.0**

* Update all modules to use the new configuration handling of py3status_. See
  the `module configuration <https://github.com/ultrabug/py3status/wiki/Load-and-order-py3status-modules-directly-from-your-current-i3status-config#configuring-a-py3status-module>`_
  section of the `py3status documentation`_ for more information.

   .. note::

      This change deprecates the ``modules.ini`` file.

* `batterystatus`: Make format strings conform to ``i3status.conf``. See
  :ref:`batterystatus_settings`.

   .. warning::

      Be sure to update your ``format`` setting accordingly if you used it
      previously.

* `mailstatus`: Make ``mailboxes`` setting conform to ``i3status.conf``. See
  :ref:`mailstatus_settings`.
   
   .. warning::
      
      Be sure to update your ``mailboxes`` setting accordingly.

* Add :ref:`alsastatus_module` module.


.. _py3status: https://github.com/ultrabug/py3status
.. _py3status documentation: https://github.com/ultrabug/py3status/wiki
