.. _installation:

Installation
============

From Source
-----------

Fetch the latest sources from github_:

.. code-block:: bash

   $ wget https://github.com/tablet-mode/py3status-modules/archive/0.2.0.tar.gz

#. Unpack the sources:

   .. code-block:: bash

      $ tar xvzf 0.2.0.tar.gz

#. Enter source directory and copy the modules you want to use to your
   ``py3status`` folder:

   .. code-block:: bash

      $ cd py3status-modules-0.2.0
      $ cp batterystatus/batterystatus.py ~/.i3/py3status/
      $ cp mailstatus/mailstatus.py ~/.i3/py3status/

#. Then rename and copy the example config to your ``py3status`` directory:

   .. code-block:: bash

      $ cp modules.ini.example ~/.i3/py3status/modules.ini

#. Adjust the ``modules.ini`` you just copied with your editor of choice:

   .. code-block:: bash

      # e.g.
      $ vi ~/.i3/py3status/modules.ini

   See :ref:`configuration` for an explanation of the configuration format and an
   example.


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

Finally copy and adjust the ``modules.ini``:

   .. code-block:: bash
      
      $ cp /usr/share/doc/py3status-modules-0.2.0/modules.ini.example \
         ~/.i3/py3status/modules.ini
   
See :ref:`configuration` for an explanation of the configuration format and an
example.


.. _github: https://github.com
.. _my-little-overlay: https://github.com/twisted-pear/my-little-overlay
.. _aur: https://aur.archlinux.org/packages/py3status-modules-tm
