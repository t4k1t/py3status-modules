.. _changelog:

Changelog
=========

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

* Add `alsastatus` module.


.. _py3status: https://github.com/ultrabug/py3status
.. _py3status documentation: https://github.com/ultrabug/py3status/wiki
