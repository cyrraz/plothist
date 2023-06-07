.. _installation-label:

============
Installation
============


Using PyPI (stable version)
===========================

1.  (Optional) If you use a local environment:

    For example, run:

    .. code-block:: bash

        source venv/bin/activate


2. Install ``plothist`` from ``PyPI`` into your environment.

   a.  If you have a local installation, you can use the normal setup command

   .. code-block:: bash

       pip3 install plothist


   b.  If this fails because you do not have write access to where your virtual environment lives, you can also install ``plothist`` locally:

   .. code-block:: bash

       pip3 install --user plothist

   This will automatically also install ``plothist`` into your current environment.
   Please make sure to always setup your environment correctly before using ``plothist``.

   The ``plothist`` package can now be imported in any of your scripts. Now you can go on with the :ref:`basics-1d_hist-label`.



Using Flit (development version)
================================

1.  (Optional) If you use a local environment:

    For example, run:

    .. code-block:: bash

        source venv/bin/activate

2.  Install flit:

    .. code-block:: bash

        pip3 install flit

3. Clone the plothist repository:

    .. code-block:: bash

        git clone git@github.com:cyrraz/plothist.git

4. Go inside the plothist folder and run:

    .. code-block:: bash

        flit install --symlink

   if it doesn't work, do:

    .. code-block:: bash

        python3 -m flit install --symlink

To update the ``plothist`` library, go to the library repository, and run ``git pull``.
