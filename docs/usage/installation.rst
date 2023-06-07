.. _installation-label:

============
Installation
============


Using PyPI
==========

soon


Using Flit (development version)
============================

1.  Install flit:

    .. code-block:: bash

        pip3 install --upgrade flit --user

2.  Install boost_histogram package:

    .. code-block:: bash

        pip3 install --upgrade boost_histogram --user

3. Clone the plothist repository:

    .. code-block:: bash

        git clone git@github.com:cyrraz/plothist.git

4. Go inside the plothist folder and run:

    .. code-block:: bash

        flit install --symlink

   if it doesn't work, do:

    .. code-block:: bash

        python3 -m flit install --symlink


The plothist library can now be imported in any of your scripts. Now you can go on with the :ref:`basics-1d_hist-label`.
To update the plothist library, go to the library repository, and run git pull.
