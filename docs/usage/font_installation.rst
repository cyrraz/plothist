.. _usage-fonts-label:

=================
Font installation
=================

Latin Modern fonts are used by default (Latin Modern Math, Latin Modern Roman, Latin Modern Sans).

On Linux/Ubuntu/MacOS, after installing ``plothist``, you can install the fonts by running on your terminal:

.. code-block:: bash

    install_latin_modern_fonts

Try to restart your python session and run ``import plothist`` again. If no warning is raised, the fonts are installed correctly and you can skip the rest of this section.

Troubleshooting
===============

If the command doesn't exist, you can run the script manually. First you need to get the folder where ``plothist`` is installed. You can do this by running in a python console:

.. code-block:: python

   import plothist
   plothist.__file__

   > '/path/to/plothist/__init__.py'

Then you can run the following command in a terminal:

.. code-block:: bash

   python3 /path/to/plothist/scripts/install_latin_modern_fonts.py

If the command doesn't work, you may read the detailed procedure directly in the `python script <https://github.com/cyrraz/plothist/blob/main/plothist/scripts/install_latin_modern_fonts.py>`_ called by the command ``install_latin_modern_fonts`` and execute the commands line by line in a terminal.

It was observed in some cases that, after the procedure above, you may need to move the font files ``latinmodern-math.otf``, ``latin-modern-roman/`` and ``latin-modern-sans/`` from ``~/.fonts/`` into another folder. To get an idea of where the fonts are installed on your system, you can run the following commands in a python console:

.. code-block:: python

   from matplotlib import font_manager
   font_manager.findSystemFonts(fontpaths=None, fontext="ttf")

Make also sure to delete the cache of matplotlib, otherwise the fonts may not be loaded correctly. You can delete the cache folder by running in a python console:

.. code-block:: python

   import matplotlib
   import subprocess
   cache_dir = matplotlib.get_cachedir()
   subprocess.run(["rm", "-rv", cache_dir])
