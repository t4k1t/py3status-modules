.. _installation:

Installation
============

From Source
-----------

Fetch the latest sources from github_:

.. code-block:: bash

   $ wget https://github.com/tablet-mode/py3status-modules/archive/0.3.0.tar.gz

#. Unpack the sources:

   .. code-block:: bash

      $ tar xvzf 0.3.0.tar.gz

#. Enter source directory and copy the modules you want to use to your
   ``py3status`` folder:

   .. code-block:: bash

      $ cd py3status-modules-0.3.0
      $ cp batterystatus/batterystatus.py ~/.i3/py3status/
      $ cp mailstatus/mailstatus.py ~/.i3/py3status/

#. Adjust your ``i3status.conf`` with your editor of choice to configure your
   new modules accordingly:

   .. code-block:: bash

      # e.g.
      $ vi ~/.i3/i3status.conf

   See :ref:`configuration` for an explanation of the configuration format and an
   example.

   .. seealso::

      `Loading a py3status module <https://github.com/ultrabug/py3status/wiki/Load-and-order-py3status-modules-directly-from-your-current-i3status-config#loading-a-py3status-module>`_ from py3status' documentation.


Distribution Specific
---------------------

The following distribution specific installation aids are available:

* Gentoo GNU/Linux: `py3stauts-modules` ebuild in the my-little-overlay_ overlay
* Arch Linux: `py3status-modules` PKGBUILD available at aur_

After installing ``py3status-modules`` you will have to put symlinks to the
modules you want to use into your ``py3status`` directory:

   .. code-block:: bash

      $ cd ~/.i3/py3status
      $ ln -s /usr/share/py3status-modules/batterystatus.py
      $ ln -s /usr/share/py3status-modules/mailstatus.py

Alternatively you can also just copy the modules, but than you will have to
remember to copy them again after each update.

Finally adjust your ``i3status.conf``:

See :ref:`configuration` for an explanation of the configuration format and an
example.

   .. seealso::

      `Loading a py3status module <https://github.com/ultrabug/py3status/wiki/Load-and-order-py3status-modules-directly-from-your-current-i3status-config#loading-a-py3status-module>`_ from py3status' documentation.


.. _github: https://github.com
.. _my-little-overlay: https://github.com/twisted-pear/my-little-overlay
.. _aur: https://aur.archlinux.org/packages/py3status-modules
